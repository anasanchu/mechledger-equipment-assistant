"""Central application configuration and environment settings for MECHLEDGER.

Loads environment variables, defines API keys, API endpoints, model parameters,
and default filesystem paths.
"""

import os
import sys
from dotenv import load_dotenv

# Ensure stdout and stderr handle UTF-8 symbols/emojis seamlessly across Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Load variables from .env file
load_dotenv()


def _configured_value(name: str, default=None):
    """Return a configured value, treating common template values as unset."""
    value = os.getenv(name, default)
    if value is None:
        return None
    value = value.strip().strip('"').strip("'")
    if not value:
        return None
    if any(marker in value.lower() for marker in ("your_", "xxxx", "replace_me", "changeme")):
        return None
    return value

# API Keys & Credentials
HF_TOKEN = _configured_value("HF_TOKEN")
GROQ_API_KEY = _configured_value("GROQ_API_KEY")
QDRANT_URL = _configured_value("QDRANT_URL", "") or ""
QDRANT_API_KEY = _configured_value("QDRANT_API_KEY", "") or ""

# Model Configurations
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
NOMIC_EMBED_MODEL = "nomic-embed-text-v1.5"  # legacy compatibility only
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_EMBED_DIMENSION = int(os.getenv("OLLAMA_EMBED_DIMENSION", "768"))
_embedding_slug = "".join(ch if ch.isalnum() else "-" for ch in OLLAMA_EMBED_MODEL.lower()).strip("-")
_embedding_collection = f"mechledger-{_embedding_slug}"
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", _embedding_collection)
VECTOR_DIMENSION = OLLAMA_EMBED_DIMENSION

# Remote API Endpoints
MINERU_API_URL = os.getenv("MINERU_API_URL", "https://abhiswork-ikb-mineru.hf.space/file_parse")
MINERU_TIMEOUT_SECONDS = int(os.getenv("MINERU_TIMEOUT_SECONDS", "300"))
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "50"))
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:3b")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Storage & File Directories
DB_PATH = f"./simple_vector_db_{_embedding_slug}.json"
UPLOAD_DIR = "uploaded_documents"
STATIC_IMAGES_DIR = "static_images"
PARSED_DATA_DIR = "parsed_data"

# Service Host & Port
API_HOST = "0.0.0.0"
API_PORT = 8002
API_BASE_URL = f"http://localhost:{API_PORT}"
