"""Filesystem helpers for document saving, artifact persistence, and directory cleanup.

Encapsulates file and folder operations for IKB-RAG.
"""

import os
import json
import base64
import shutil
from typing import Dict, Any
from config.settings import UPLOAD_DIR, STATIC_IMAGES_DIR, PARSED_DATA_DIR


def ensure_dir(path: str) -> None:
    """Ensure that the given directory exists."""
    os.makedirs(path, exist_ok=True)


def copy_document(file_path: str, chat_id: str) -> tuple[str, str, str]:
    """Copies document into uploaded_documents with chat_id prefix if needed.
    
    Returns:
        tuple: (base_name, doc_name, saved_doc_path)
    """
    base_name = os.path.basename(file_path)
    if not base_name.startswith(f"{chat_id}_"):
        doc_name = f"{chat_id}_{base_name}"
    else:
        doc_name = base_name

    ensure_dir(UPLOAD_DIR)
    saved_doc_path = os.path.abspath(os.path.join(UPLOAD_DIR, doc_name))
    shutil.copy(file_path, saved_doc_path)
    return base_name, doc_name, saved_doc_path


def save_parsed_artifacts(parsed_data: Any, text: str, chat_id: str, pdf_base: str) -> str:
    """Saves MinerU raw output JSON and markdown content to parsed_data directory."""
    parsed_dir = os.path.join(PARSED_DATA_DIR, str(chat_id), pdf_base)
    ensure_dir(parsed_dir)

    with open(os.path.join(parsed_dir, "mineru_output.json"), "w", encoding="utf-8") as f:
        json_to_save = parsed_data
        if isinstance(parsed_data, dict) and "data" in parsed_data and "content_list" in parsed_data["data"]:
            if parsed_data["data"]["content_list"]:
                json_to_save = parsed_data["data"]["content_list"]
        json.dump(json_to_save, f, indent=2, ensure_ascii=False)

    with open(os.path.join(parsed_dir, "content.md"), "w", encoding="utf-8") as f:
        f.write(text)

    return parsed_dir


def save_base64_images(images_dict: Dict[str, str], chat_id: str, pdf_base: str) -> str:
    """Decodes base64-encoded images from MinerU response and writes them to static_images."""
    img_dir = os.path.join(STATIC_IMAGES_DIR, str(chat_id), pdf_base)
    ensure_dir(img_dir)
    for img_name, b64_data in images_dict.items():
        img_bytes = base64.b64decode(b64_data)
        clean_name = os.path.basename(img_name)
        with open(os.path.join(img_dir, clean_name), "wb") as f:
            f.write(img_bytes)
    return img_dir


def delete_chat_files(chat_id: str) -> None:
    """Removes all filesystem artifacts for a specific chat_id."""
    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            if filename.startswith(f"{chat_id}_"):
                try:
                    os.remove(os.path.join(UPLOAD_DIR, filename))
                except Exception:
                    pass

    chat_images_dir = os.path.join(STATIC_IMAGES_DIR, str(chat_id))
    if os.path.exists(chat_images_dir):
        try:
            shutil.rmtree(chat_images_dir)
        except Exception:
            pass

    chat_parsed_dir = os.path.join(PARSED_DATA_DIR, str(chat_id))
    if os.path.exists(chat_parsed_dir):
        try:
            shutil.rmtree(chat_parsed_dir)
        except Exception:
            pass


def clear_all_storage_directories() -> None:
    """Removes all document uploads, static images, and parsed artifacts."""
    for folder in [UPLOAD_DIR, STATIC_IMAGES_DIR, PARSED_DATA_DIR]:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except Exception:
                pass
