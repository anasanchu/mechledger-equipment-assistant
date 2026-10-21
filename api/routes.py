"""FastAPI HTTP endpoint routes for IKB-RAG.

Exposes query, upload, document viewing, diagram serving, and chat data management.
"""

import os
import glob
import traceback
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from api.schemas import (
    QueryRequest,
    QueryResponse,
    UploadResponse,
    DocumentListResponse,
    MessageResponse,
)
from src.ikb_rag import rag_engine
from config.settings import UPLOAD_DIR, STATIC_IMAGES_DIR

router = APIRouter()


@router.get("/")
async def root():
    return {"status": "online", "service": "IKB-RAG API", "docs": "/docs"}


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    try:
        response = rag_engine.query(req.question, req.chat_id)
        return {"answer": response}
    except Exception as e:
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=UploadResponse)
async def upload_document(chat_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Save the file temporarily to pass to the rag_engine
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    content = await file.read()
    with open(temp_path, "wb") as f:
        f.write(content)

    try:
        num_chunks = rag_engine.index_document(temp_path, chat_id)
        return {
            "message": f"Document {file.filename} processed! {num_chunks} chunks indexed.",
            "filename": file.filename
        }
    except Exception as e:
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the un-prefixed temp file if it wasn't moved
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(chat_id: str = "default"):
    docs = []
    if os.path.exists(UPLOAD_DIR):
        for path in glob.glob(f"{UPLOAD_DIR}/{chat_id}_*"):
            basename = os.path.basename(path)
            # Remove chat_id_ prefix for display
            clean_name = basename[len(f"{chat_id}_"):]
            docs.append(clean_name)
    return {"documents": docs}


@router.get("/documents/{chat_id}/{filename}")
async def get_document(chat_id: str, filename: str):
    file_path = os.path.join(UPLOAD_DIR, f"{chat_id}_{filename}")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")


@router.get("/images/{chat_id}/{pdf_base}/{filename}")
async def get_image(chat_id: str, pdf_base: str, filename: str):
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
    msg = rag_engine.delete_chat_data(chat_id)
    return {"message": msg}


@router.post("/chat/{chat_id}/refresh", response_model=MessageResponse)
async def refresh_chat(chat_id: str):
    try:
        msg = rag_engine.refresh_chat_data(chat_id)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear", response_model=MessageResponse)
async def clear_kb():
    msg = rag_engine.clear_knowledge_base()
    return {"message": msg}
