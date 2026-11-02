"""FastAPI HTTP endpoint routes for MECHLEDGER.

Exposes query, upload, document viewing, diagram serving, and chat data management.
"""

import os
import glob
import traceback
import re
import uuid
import shutil
import io
import zipfile
import logging
from threading import Lock
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, Response
from api.schemas import (
    QueryRequest,
    QueryResponse,
    UploadResponse,
    DocumentListResponse,
    MessageResponse,
    ReportRequest,
)
from api.reporting import build_report_pdf
from src.ikb_rag import rag_engine
from config.settings import UPLOAD_DIR, STATIC_IMAGES_DIR, PARSED_DATA_DIR, MAX_UPLOAD_MB

router = APIRouter()
logger = logging.getLogger(__name__)
_document_jobs = {}
_document_locks = {}
_document_jobs_lock = Lock()


@router.get("/")
async def root():
    return {"status": "online", "service": "MECHLEDGER API", "docs": "/docs"}


def _valid_chat_id(chat_id: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{1,64}", chat_id or ""))


def _processing_message(error: Exception) -> str:
    text = str(error).lower()
    if "timeout" in text or "timed out" in text or "connection aborted" in text:
        return "The file is saved, but the document reader timed out. Try a smaller PDF or retry in a few minutes."
    if "ollama" in text or "embedding" in text:
        return "The file is saved, but the search index could not be built. Check that Ollama is running, then retry."
    return "The file is saved, but it could not be prepared for search. Retry in a few minutes."


def _run_document_index(chat_id: str, filename: str, saved_path: str, token: str) -> None:
    key = (chat_id, filename)
    with _document_jobs_lock:
        document_lock = _document_locks.setdefault(key, Lock())

    with document_lock:
        with _document_jobs_lock:
            current = _document_jobs.get(key)
            if current is not None and current.get("token") != token:
                return
            if current is None:
                cancelled_before_start = True
            else:
                cancelled_before_start = False
        if cancelled_before_start:
            if os.path.exists(saved_path):
                try:
                    os.remove(saved_path)
                except OSError:
                    logger.exception("Could not remove cancelled upload %s", filename)
            return

        try:
            chunks = rag_engine.index_document(saved_path, chat_id)
            with _document_jobs_lock:
                current = _document_jobs.get(key)
                still_current = current is not None and current.get("token") == token
                deleted = current is None
                if still_current:
                    _document_jobs[key] = {"status": "ready", "message": f"Ready to search ({chunks} sections)."}
            if deleted:
                # The user removed this file while it was processing.
                try:
                    rag_engine.active_store.delete_document(chat_id, filename)
                except Exception:
                    logger.exception("Could not remove vectors for cancelled document %s", filename)
                try:
                    if os.path.exists(saved_path):
                        os.remove(saved_path)
                except OSError:
                    logger.exception("Could not remove cancelled upload %s", filename)
                base = os.path.splitext(filename)[0]
                shutil.rmtree(os.path.join(PARSED_DATA_DIR, chat_id, base), ignore_errors=True)
                shutil.rmtree(os.path.join(STATIC_IMAGES_DIR, chat_id, base), ignore_errors=True)
        except Exception as exc:
            logger.exception("Document processing failed for %s", filename)
            with _document_jobs_lock:
                current = _document_jobs.get(key)
                if current is not None and current.get("token") == token:
                    _document_jobs[key] = {"status": "failed", "message": _processing_message(exc)}


def _schedule_document_index(background_tasks: BackgroundTasks, chat_id: str, filename: str, saved_path: str) -> str:
    key = (chat_id, filename)
    with _document_jobs_lock:
        current = _document_jobs.get(key)
        if current and current.get("status") == "processing":
            raise HTTPException(status_code=409, detail="This manual is already being prepared.")
        token = uuid.uuid4().hex
        _document_jobs[key] = {"status": "processing", "message": "Preparing your manual for search.", "token": token}
    background_tasks.add_task(_run_document_index, chat_id, filename, saved_path, token)
    return token


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    try:
        if not _valid_chat_id(req.chat_id):
            raise HTTPException(status_code=400, detail="Invalid workspace identifier")
        question = req.question
        if req.equipment_context.strip():
            question = (
                "Operator-supplied equipment context (treat as unverified user input):\n"
                f"{req.equipment_context.strip()}\n\nReported issue: {req.question}"
            )
        response = rag_engine.query(question, req.chat_id)
        return {"answer": response}
    except Exception as e:
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=UploadResponse)
async def upload_document(background_tasks: BackgroundTasks, chat_id: str = Form(...), file: UploadFile = File(...)):
    if not _valid_chat_id(chat_id):
        raise HTTPException(status_code=400, detail="Invalid workspace identifier")
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    filename = file.filename.replace("\\", "/").split("/")[-1].strip()
    filename = re.sub(r'[\x00-\x1f<>:"|?*]', "_", filename).rstrip(" .")
    extension = os.path.splitext(filename)[1].lower()
    if not filename or extension not in {".pdf", ".docx", ".txt"}:
        raise HTTPException(status_code=400, detail="Upload a PDF, DOCX, or TXT technical document")
    saved_path = os.path.join(UPLOAD_DIR, f"{chat_id}_{filename}")
    if os.path.exists(saved_path):
        raise HTTPException(status_code=409, detail="A document with this filename is already in this case. Rename the PDF before uploading it again.")

    content = bytearray()
    while chunk := await file.read(1024 * 1024):
        content.extend(chunk)
        if len(content) > MAX_UPLOAD_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"File exceeds the {MAX_UPLOAD_MB} MB upload limit")
    if extension == ".pdf" and not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF")
    if extension == ".docx":
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as docx:
                if "word/document.xml" not in docx.namelist():
                    raise ValueError("Missing Word document content")
        except (zipfile.BadZipFile, ValueError):
            raise HTTPException(status_code=400, detail="The uploaded file is not a valid DOCX")
    if extension == ".txt":
        try:
            content.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="TXT documents must use UTF-8 encoding")

    # Stage under a unique directory to prevent concurrent name collisions.
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    staging_dir = os.path.join(UPLOAD_DIR, ".staging", uuid.uuid4().hex)
    os.makedirs(staging_dir, exist_ok=True)
    temp_path = os.path.join(staging_dir, filename)

    with open(temp_path, "wb") as f:
        f.write(content)

    try:
        # Save the original before calling the remote parser. If the parser is
        # unavailable, the user can still see the file and retry processing.
        os.replace(temp_path, saved_path)
        _schedule_document_index(background_tasks, chat_id, filename, saved_path)
        return {
            "message": "Manual saved. Preparing it for search now.",
            "filename": filename,
            "status": "processing",
        }
    except Exception:
        if os.path.exists(saved_path) and not os.path.exists(temp_path):
            try:
                os.remove(saved_path)
            except OSError:
                pass
        raise
    finally:
        # Clean up the un-prefixed temp file if it wasn't moved
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
        try:
            os.rmdir(staging_dir)
            os.rmdir(os.path.dirname(staging_dir))
        except OSError:
            pass


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(chat_id: str = "default"):
    if not _valid_chat_id(chat_id):
        raise HTTPException(status_code=400, detail="Invalid workspace identifier")
    docs = []
    if os.path.exists(UPLOAD_DIR):
        for path in glob.glob(f"{UPLOAD_DIR}/{chat_id}_*"):
            basename = os.path.basename(path)
            # Remove chat_id_ prefix for display
            clean_name = basename[len(f"{chat_id}_"):]
            docs.append(clean_name)
    return {"documents": docs}


@router.get("/documents/status")
async def document_status(chat_id: str = "default"):
    if not _valid_chat_id(chat_id):
        raise HTTPException(status_code=400, detail="Invalid workspace identifier")
    documents = await list_documents(chat_id)
    warning = ""
    try:
        indexed = rag_engine.active_store.list_indexed_documents(chat_id)
    except Exception:
        logger.exception("Could not check indexed documents for case %s", chat_id)
        indexed = set()
        warning = "Search status is temporarily unavailable. Your saved files are still listed."
    with _document_jobs_lock:
        jobs = {name: dict(value) for (job_chat, name), value in _document_jobs.items() if job_chat == chat_id}
    return {
        "documents": [
            {
                "filename": name,
                "indexed": name in indexed,
                "status": "ready" if name in indexed else jobs.get(name, {}).get("status", "needs_retry"),
                "message": "Ready to search." if name in indexed else jobs.get(name, {}).get("message", "Saved, but not indexed yet."),
            }
            for name in documents["documents"]
        ],
        "warning": warning,
    }


@router.post("/documents/{chat_id}/{filename}/process", response_model=MessageResponse)
async def retry_document_processing(chat_id: str, filename: str, background_tasks: BackgroundTasks):
    if not _valid_chat_id(chat_id) or filename != os.path.basename(filename):
        raise HTTPException(status_code=400, detail="Invalid document path")
    saved_path = os.path.join(UPLOAD_DIR, f"{chat_id}_{filename}")
    if not os.path.isfile(saved_path):
        raise HTTPException(status_code=404, detail="This manual is not saved in this case.")
    _schedule_document_index(background_tasks, chat_id, filename, saved_path)
    return {"message": "Retry started. This manual is being prepared for search."}


@router.get("/documents/{chat_id}/{filename}")
async def get_document(chat_id: str, filename: str):
    if not _valid_chat_id(chat_id) or filename != os.path.basename(filename):
        raise HTTPException(status_code=400, detail="Invalid document path")
    file_path = os.path.join(UPLOAD_DIR, f"{chat_id}_{filename}")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")


@router.delete("/documents/{chat_id}/{filename}", response_model=MessageResponse)
async def delete_document(chat_id: str, filename: str):
    if not _valid_chat_id(chat_id) or filename != os.path.basename(filename):
        raise HTTPException(status_code=400, detail="Invalid document path")
    file_path = os.path.join(UPLOAD_DIR, f"{chat_id}_{filename}")
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    with _document_jobs_lock:
        _document_jobs.pop((chat_id, filename), None)
    vector_warning = ""
    try:
        rag_engine.active_store.delete_document(chat_id, filename)
    except Exception:
        logger.exception("Could not remove vectors for document %s", filename)
        vector_warning = " Search cleanup may finish after the index service reconnects."
    try:
        os.remove(file_path)
        pdf_base = os.path.splitext(filename)[0]
        shutil.rmtree(os.path.join(PARSED_DATA_DIR, chat_id, pdf_base), ignore_errors=True)
        shutil.rmtree(os.path.join(STATIC_IMAGES_DIR, chat_id, pdf_base), ignore_errors=True)
        return {"message": f"Removed {filename} from this case.{vector_warning}"}
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"The manual could not be removed from storage: {exc}")


@router.get("/images/{chat_id}/{pdf_base}/{filename}")
async def get_image(chat_id: str, pdf_base: str, filename: str):
    if not _valid_chat_id(chat_id) or any(part != os.path.basename(part) for part in (pdf_base, filename)):
        raise HTTPException(status_code=400, detail="Invalid image path")
    base_dir = os.path.join(STATIC_IMAGES_DIR, str(chat_id), pdf_base)
    # Strip extension from the requested filename
    name_without_ext = os.path.splitext(filename)[0]

    # Search for any file with that name regardless of extension
    search_pattern = os.path.join(base_dir, f"{name_without_ext}.*")
    matches = glob.glob(search_pattern)

    if matches:
        return FileResponse(matches[0])

    raise HTTPException(status_code=404, detail="Image not found")


@router.delete("/chat/{chat_id}", response_model=MessageResponse)
async def delete_chat(chat_id: str):
    if not _valid_chat_id(chat_id):
        raise HTTPException(status_code=400, detail="Invalid workspace identifier")
    with _document_jobs_lock:
        for key in [key for key in _document_jobs if key[0] == chat_id]:
            _document_jobs.pop(key, None)
    try:
        msg = rag_engine.delete_chat_data(chat_id)
        return {"message": msg}
    except Exception as exc:
        logger.exception("Could not fully clear server data for case %s", chat_id)
        from src.ikb_rag.utils.file_utils import delete_chat_files
        delete_chat_files(chat_id)
        raise HTTPException(status_code=503, detail="The conversation was removed in the browser, but server cleanup needs to be retried.") from exc


@router.post("/chat/{chat_id}/refresh", response_model=MessageResponse)
async def refresh_chat(chat_id: str):
    if not _valid_chat_id(chat_id):
        raise HTTPException(status_code=400, detail="Invalid workspace identifier")
    try:
        msg = rag_engine.refresh_chat_data(chat_id)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reports/{chat_id}")
async def create_report(chat_id: str, report: ReportRequest):
    if not _valid_chat_id(chat_id):
        raise HTTPException(status_code=400, detail="Invalid workspace identifier")
    try:
        report_data = report.model_dump() if hasattr(report, "model_dump") else report.dict()
        pdf = build_report_pdf(report_data)
        safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", chat_id)
        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="MECHLEDGER-{safe_id}-report.pdf"'},
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {exc}")


@router.post("/clear", response_model=MessageResponse)
async def clear_kb():
    msg = rag_engine.clear_knowledge_base()
    return {"message": msg}
