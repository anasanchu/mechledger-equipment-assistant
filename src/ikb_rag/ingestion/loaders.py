"""Document loader and parser integrating MinerU multimodal extraction.

Sends industrial documents (PDF, DOCX, TXT) to the MinerU parsing service,
extracts text and tables, and saves high-resolution diagrams.
"""

import os
import json
import requests
import shutil
import base64
from typing import Dict, Any, Tuple
from config.settings import HF_TOKEN, MINERU_API_URL, UPLOAD_DIR, PARSED_DATA_DIR, STATIC_IMAGES_DIR, API_PORT


class MinerUDocumentLoader:
    """Loads documents and queries the remote MinerU parser for structured multimodal extraction."""

    def __init__(self, hf_token: str = None, api_url: str = None):
        self.hf_token = hf_token or HF_TOKEN
        self.api_url = api_url or MINERU_API_URL

    def load_and_parse(self, file_path: str, chat_id: str = "default") -> Tuple[Any, str, str, str, str]:
        """Loads a file, sends it to MinerU, persists parsed artifacts, and saves extracted images.
        
        Returns:
            Tuple of (parsed_data, text, base_name, pdf_base, doc_url)
        """
        print("\n" + "=" * 50)
        print("📄 MINERU PROCESSING STATUS")
        print("=" * 50)
        print("🟢 Prepare: Initializing document processing...")
        print(f"Loading document: {file_path} for chat: {chat_id}")

        try:
            base_name = os.path.basename(file_path)
            if not base_name.startswith(f"{chat_id}_"):
                doc_name = f"{chat_id}_{base_name}"
            else:
                doc_name = base_name

            os.makedirs(UPLOAD_DIR, exist_ok=True)
            saved_doc_path = os.path.abspath(os.path.join(UPLOAD_DIR, doc_name))
            shutil.copy(file_path, saved_doc_path)

            print("🟢 Check service: Verifying MinerU API...")
            print("🟢 Submit: Uploading file to MinerU...")
            print(f"Sending document to MinerU: {self.api_url}")
            print("🟡 Parse: MinerU is extracting text and tables (this may take a while)...")

            with open(file_path, "rb") as f:
                files = {"files": (doc_name, f)}
                data = {"is_ocr": "False", "backend": "pipeline"}
                headers = {"Authorization": f"Bearer {self.hf_token}"}
                res = requests.post(self.api_url, files=files, data=data, headers=headers)

            print("🟢 Parse: Extraction complete!")
            print("🟢 Download: Retrieving JSON payload...")
            if res.status_code != 200:
                raise Exception(f"MinerU API Error: HTTP {res.status_code} - {res.text}")

            parsed_data = res.json()

            text = ""
            if isinstance(parsed_data, dict):
                if "content" in parsed_data:
                    text = parsed_data["content"]
                elif "data" in parsed_data and "markdown" in parsed_data["data"]:
                    text = parsed_data["data"]["markdown"]
                elif "markdown" in parsed_data:
                    text = parsed_data["markdown"]
                else:
                    text = json.dumps(parsed_data, indent=2)
            else:
                text = str(parsed_data)

            pdf_base = os.path.splitext(base_name)[0]
            parsed_dir = os.path.join(PARSED_DATA_DIR, str(chat_id), pdf_base)
            os.makedirs(parsed_dir, exist_ok=True)

            with open(os.path.join(parsed_dir, "mineru_output.json"), "w", encoding="utf-8") as f:
                json_to_save = parsed_data
                if isinstance(parsed_data, dict) and "data" in parsed_data and "content_list" in parsed_data["data"]:
                    if parsed_data["data"]["content_list"]:
                        json_to_save = parsed_data["data"]["content_list"]
                json.dump(json_to_save, f, indent=2, ensure_ascii=False)

            with open(os.path.join(parsed_dir, "content.md"), "w", encoding="utf-8") as f:
                f.write(text)

            if isinstance(parsed_data, dict) and "data" in parsed_data and "images_base64" in parsed_data["data"]:
                img_dir = os.path.join(STATIC_IMAGES_DIR, str(chat_id), pdf_base)
                os.makedirs(img_dir, exist_ok=True)
                for img_name, b64_data in parsed_data["data"]["images_base64"].items():
                    img_bytes = base64.b64decode(b64_data)
                    clean_name = os.path.basename(img_name)
                    with open(os.path.join(img_dir, clean_name), "wb") as f:
                        f.write(img_bytes)

            doc_url = f"http://localhost:{API_PORT}/documents/{chat_id}/{base_name}"
            return parsed_data, text, base_name, pdf_base, doc_url

        except Exception as e:
            raise Exception(f"Failed to process file {file_path}. Error: {str(e)}")
