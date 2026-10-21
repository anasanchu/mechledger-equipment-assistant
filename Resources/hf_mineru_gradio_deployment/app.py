import os
import shutil
import tempfile
import subprocess
import json
import base64
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="MinerU Parsing API")

@app.post("/file_parse")
async def file_parse(
    request: Request,
    files: UploadFile = File(...),
    is_ocr: str = Form("False"),
    backend: str = Form("pipeline")
):
    # Authenticate the API route using the SPACE_API_KEY
    expected_key = os.environ.get("SPACE_API_KEY", "")
    if expected_key:
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {expected_key}":
            raise HTTPException(status_code=401, detail="Unauthorized")

    # Create temporary environment
    output_dir = tempfile.mkdtemp()
    file_path = os.path.join(output_dir, files.filename)
    
    content = await files.read()
    with open(file_path, "wb") as f:
        f.write(content)

    env = os.environ.copy()
    env["MINERU_BACKEND"] = backend
    env["MINERU_DEVICE_MODE"] = "cpu"

    # Command construction
    command = ["mineru", "-p", file_path, "-o", output_dir, "--backend", backend]
    if str(is_ocr).lower() == "true":
        command.append("--is-ocr")

    try:
        process = subprocess.run(command, capture_output=True, text=True, env=env)
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"MinerU failed: {process.stderr}\n{process.stdout}")

        pdf_name = os.path.splitext(os.path.basename(file_path))[0]
        result_dir = os.path.join(output_dir, pdf_name)

        md_content = ""
        json_content_list = []
        images_base64 = {}
        
        if os.path.exists(output_dir):
            for root, _, filenames in os.walk(output_dir):
                for file in filenames:
                    if file.endswith(".md"):
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            md_content = f.read()
                    elif file.endswith("_content_list.json"):
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            try:
                                json_content_list = json.load(f)
                            except json.JSONDecodeError:
                                pass
                    elif file.lower().endswith((".jpg", ".jpeg", ".png")):
                        with open(os.path.join(root, file), "rb") as f:
                            encoded = base64.b64encode(f.read()).decode("utf-8")
                            images_base64[file] = encoded

        return JSONResponse({
            "code": 0,
            "msg": "success",
            "data": {
                "markdown": md_content,
                "content_list": json_content_list,
                "images_base64": images_base64
            }
        })
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)

@app.get("/")
def health_check():
    return {"status": "MinerU API is running! Endpoint is at POST /file_parse"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
