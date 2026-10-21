import os
import glob
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pikerag.utils.rag_utils import rag_engine

app = FastAPI(title="IKB-RAG API")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    chat_id: str = "default"

@app.post("/query")
async def query_endpoint(req: QueryRequest):
    try:
        response = rag_engine.query(req.question, req.chat_id)
        return {"answer": response}
    except Exception as e:
        import traceback
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(chat_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Save the file temporarily to pass to the rag_engine
    temp_path = os.path.join("uploaded_documents", file.filename)
    os.makedirs("uploaded_documents", exist_ok=True)
    
    content = await file.read()
    with open(temp_path, "wb") as f:
        f.write(content)
        
    try:
        num_chunks = rag_engine.index_document(temp_path, chat_id)
        return {"message": f"Document {file.filename} processed! {num_chunks} chunks indexed.", "filename": file.filename}
    except Exception as e:
        import traceback
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the un-prefixed temp file if it wasn't moved
        if os.path.exists(temp_path):
            try: os.remove(temp_path)
            except: pass

@app.get("/documents")
async def list_documents(chat_id: str = "default"):
    docs = []
    if os.path.exists("uploaded_documents"):
        for path in glob.glob(f"uploaded_documents/{chat_id}_*"):
            basename = os.path.basename(path)
            # Remove chat_id_ prefix for display
            clean_name = basename[len(f"{chat_id}_"):]
            docs.append(clean_name)
    return {"documents": docs}

@app.get("/documents/{chat_id}/{filename}")
async def get_document(chat_id: str, filename: str):
    file_path = os.path.join("uploaded_documents", f"{chat_id}_{filename}")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/images/{chat_id}/{pdf_base}/{filename}")
async def get_image(chat_id: str, pdf_base: str, filename: str):
    import glob
    base_dir = os.path.join("static_images", str(chat_id), pdf_base)
    # Strip extension from the requested filename
    name_without_ext = os.path.splitext(filename)[0]
    
    # Search for any file with that name regardless of extension
    search_pattern = os.path.join(base_dir, f"{name_without_ext}.*")
    matches = glob.glob(search_pattern)
    
    if matches:
        return FileResponse(matches[0])
        
    raise HTTPException(status_code=404, detail="Image not found")

@app.delete("/chat/{chat_id}")
async def delete_chat(chat_id: str):
    msg = rag_engine.delete_chat_data(chat_id)
    return {"message": msg}

@app.post("/chat/{chat_id}/refresh")
async def refresh_chat(chat_id: str):
    try:
        msg = rag_engine.refresh_chat_data(chat_id)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_kb():
    msg = rag_engine.clear_knowledge_base()
    return {"message": msg}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
