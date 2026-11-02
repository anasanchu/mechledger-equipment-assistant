"""Document loader and parser integrating MinerU multimodal extraction.

Sends industrial documents (PDF, DOCX, TXT) to the MinerU parsing service,
extracts text and tables, and saves high-resolution diagrams.
"""

import os
import json
import requests
import shutil
import base64
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, Any, Tuple
from config.settings import HF_TOKEN, MINERU_API_URL, MINERU_TIMEOUT_SECONDS, UPLOAD_DIR, PARSED_DATA_DIR, STATIC_IMAGES_DIR, API_PORT


class MinerUDocumentLoader:
    """Loads documents and queries the remote MinerU parser for structured multimodal extraction."""

    def __init__(self, hf_token: str = None, api_url: str = None, timeout_seconds: int = None):
        self.hf_token = hf_token or HF_TOKEN
        self.api_url = api_url or MINERU_API_URL
        self.timeout_seconds = timeout_seconds or MINERU_TIMEOUT_SECONDS

    @staticmethod
    def _extract_text_locally(file_path: str, extension: str) -> Tuple[Any, str]:
        """Extract searchable text without a remote parser when possible."""
        if extension == ".pdf":
            from pypdf import PdfReader

            content_list = []
            pages = []
            reader = PdfReader(file_path, strict=False)
            for page_idx, page in enumerate(reader.pages):
                page_text = (page.extract_text() or "").strip()
                if page_text:
                    pages.append(page_text)
                    content_list.append({"type": "text", "text": page_text, "page_idx": page_idx})
            text = "\n\n".join(pages)
            if not text.strip():
                raise ValueError("This PDF has no selectable text. It may be scanned and need OCR.")
            return {"data": {"content_list": content_list}, "local_text_fallback": True}, text

        if extension == ".txt":
            with open(file_path, "r", encoding="utf-8-sig") as source:
                text = source.read().strip()
            if not text:
                raise ValueError("This text file is empty.")
            blocks = [
                {"type": "text", "text": line.strip(), "page_idx": 0}
                for line in text.splitlines()
                if line.strip()
            ]
            return {"data": {"content_list": blocks}, "local_text_fallback": True}, text

        if extension == ".docx":
            namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            with zipfile.ZipFile(file_path) as document:
                root = ET.fromstring(document.read("word/document.xml"))
            paragraphs = []
            for paragraph in root.findall(".//w:p", namespace):
                value = "".join(node.text or "" for node in paragraph.findall(".//w:t", namespace)).strip()
                if value:
                    paragraphs.append(value)
            text = "\n\n".join(paragraphs)
            if not text:
                raise ValueError("This Word file contains no readable text.")
            blocks = [{"type": "text", "text": paragraph, "page_idx": 0} for paragraph in paragraphs]
            return {"data": {"content_list": blocks}, "local_text_fallback": True}, text

        raise ValueError("Local text reading is not available for this file type.")

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
            stored_name = os.path.basename(file_path)
            prefix = f"{chat_id}_"
            # Keep the externally visible source filename stable when a stored
            # case PDF is re-indexed from its already-prefixed storage path.
            base_name = stored_name[len(prefix):] if stored_name.startswith(prefix) else stored_name
            doc_name = stored_name if stored_name.startswith(prefix) else f"{prefix}{stored_name}"

            os.makedirs(UPLOAD_DIR, exist_ok=True)
            saved_doc_path = os.path.abspath(os.path.join(UPLOAD_DIR, doc_name))
            if os.path.abspath(file_path) != saved_doc_path:
                shutil.copy(file_path, saved_doc_path)

            parsed_data, text = None, ""
            try:
                print("🟢 Submit: Sending document to the document reader...")
                headers = {"Authorization": f"Bearer {self.hf_token}"} if self.hf_token else {}
                with open(file_path, "rb") as f:
                    res = requests.post(
                        self.api_url,
                        files={"files": (doc_name, f)},
                        data={"is_ocr": "False", "backend": "pipeline"},
                        headers=headers,
                        timeout=(30, self.timeout_seconds),
                    )
                if res.status_code != 200:
                    raise RuntimeError(f"Document reader returned HTTP {res.status_code}")
                parsed_data = res.json()
                if isinstance(parsed_data, dict):
                    if "content" in parsed_data:
                        text = str(parsed_data["content"])
                    elif isinstance(parsed_data.get("data"), dict) and "markdown" in parsed_data["data"]:
                        text = str(parsed_data["data"]["markdown"])
                    elif "markdown" in parsed_data:
                        text = str(parsed_data["markdown"])
                    else:
                        text = json.dumps(parsed_data, indent=2)
                else:
                    text = str(parsed_data)
                print("🟢 Document reader finished.")
            except Exception as reader_error:
                print(f"🟠 Remote reader unavailable; trying local text extraction: {reader_error}")
                try:
                    parsed_data, text = self._extract_text_locally(file_path, os.path.splitext(file_path)[1].lower())
                    print("🟢 Local text extraction finished. Diagrams and OCR are not included in fallback mode.")
                except Exception as local_error:
                    raise RuntimeError(
                        f"Document reader unavailable ({reader_error}); local text extraction could not read this file ({local_error})."
                    ) from local_error

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
