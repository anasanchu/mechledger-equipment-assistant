"""Index manager coordinating storage operations, data refreshment, and lifecycle management.

Handles refreshing, deleting, and clearing vector collections and file assets.
"""

import os
from typing import Callable, Any, Union
from src.ikb_rag.vectorstore.qdrant_store import QdrantStore
from src.ikb_rag.vectorstore.simple_json_store import SimpleJsonStore
from src.ikb_rag.utils.file_utils import delete_chat_files, clear_all_storage_directories
from config.settings import UPLOAD_DIR


class IndexManager:
    """Coordinates indexing operations across vector stores and filesystem assets."""

    def __init__(self, store: Union[QdrantStore, SimpleJsonStore]):
        self.store = store

    def refresh_chat_data(self, chat_id: str, index_document_fn: Callable[[str, str], int]) -> str:
        """Re-indexes all previously uploaded files for a specific chat_id."""
        self.store.delete_chat(chat_id)

        reindexed = 0
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                if filename.startswith(f"{chat_id}_"):
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    reindexed += index_document_fn(file_path, chat_id)

        return f"✅ Successfully re-parsed {reindexed} chunks for chat {chat_id}"

    def delete_chat_data(self, chat_id: str) -> str:
        """Deletes all indexed vectors and cached files for a specific chat_id."""
        self.store.delete_chat(chat_id)
        delete_chat_files(chat_id)
        return f"✅ Erased all data for chat {chat_id}"

    def clear_knowledge_base(self) -> str:
        """Wipes the entire vector store and cleans all file storage directories."""
        self.store.clear()
        clear_all_storage_directories()
        return "✅ Successfully erased Vector DB and File Storage!"
