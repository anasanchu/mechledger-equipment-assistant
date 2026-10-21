"""Central application configuration and environment settings for IKB-RAG.

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

# API Keys & Credentials
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NOMIC_API_KEY = os.getenv("NOMIC_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

# Model Configurations
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
NOMIC_EMBED_MODEL = "nomic-embed-text-v1.5"
QDRANT_COLLECTION_NAME = "nomic-manual"
VECTOR_DIMENSION = 768

# Remote API Endpoints
MINERU_API_URL = "https://abhiswork-ikb-mineru.hf.space/file_parse"
NOMIC_API_URL = "https://api-atlas.nomic.ai/v1/embedding/text"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Storage & File Directories
DB_PATH = "./simple_vector_db.json"
UPLOAD_DIR = "uploaded_documents"
STATIC_IMAGES_DIR = "static_images"
PARSED_DATA_DIR = "parsed_data"

# Service Host & Port
API_HOST = "0.0.0.0"
API_PORT = 8002
API_BASE_URL = f"http://localhost:{API_PORT}"
