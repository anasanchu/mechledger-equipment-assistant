"""Local JSON-based vector store fallback and pure Python cosine similarity.

Used when Qdrant Cloud is not reachable or not configured.
"""

import os
import json
import math
from typing import List, Dict, Any
from config.settings import DB_PATH


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Pure Python Cosine Similarity (No Numpy/C++ needed!)."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude1 = math.sqrt(sum(a * a for a in v1))
    magnitude2 = math.sqrt(sum(b * b for b in v2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)


class SimpleJsonStore:
    """Manages an in-memory knowledge base persisted to a local JSON file."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.knowledge_base: List[Dict[str, Any]] = []
        self.load()

    def load(self) -> None:
        """Loads records from the JSON database file if present."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.knowledge_base = json.load(f)
            except Exception:
                self.knowledge_base = []

    def save(self) -> None:
        """Persists the in-memory knowledge base to the JSON database file."""
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.knowledge_base, f)

    def add_documents(self, payloads: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        """Adds document payloads and their corresponding vector embeddings."""
        for i, emb in enumerate(embeddings):
            doc_record = payloads[i].copy()
            doc_record["embedding"] = emb
            self.knowledge_base.append(doc_record)
        self.save()

    def search(self, query_embedding: List[float], chat_id: str, limit: int = 6) -> List[Dict[str, Any]]:
        """Performs linear scan cosine similarity search filtered by chat_id."""
        scores = []
        for doc in self.knowledge_base:
            if doc.get("chat_id") == chat_id:
                score = cosine_similarity(query_embedding, doc["embedding"])
                scores.append((score, doc))
        scores.sort(reverse=True, key=lambda x: x[0])
        return [doc for score, doc in scores[:limit]]

    def delete_chat(self, chat_id: str) -> None:
        """Removes all documents belonging to the specified chat_id."""
        self.knowledge_base = [doc for doc in self.knowledge_base if doc.get("chat_id") != chat_id]
        if os.path.exists(self.db_path):
            self.save()

    def clear(self) -> None:
        """Wipes the in-memory list and deletes the JSON file."""
        self.knowledge_base = []
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass
