"""Local JSON-based vector store fallback and pure Python cosine similarity.

Used when Qdrant Cloud is not reachable or not configured.
"""

import os
import json
import math
import glob
from typing import List, Dict, Any
from config.settings import DB_PATH, OLLAMA_EMBED_MODEL


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
        self.embedding_model = OLLAMA_EMBED_MODEL
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
            doc_record["embedding_model"] = self.embedding_model
            self.knowledge_base.append(doc_record)
        self.save()

    def search(self, query_embedding: List[float], chat_id: str, limit: int = 6, embedding_model: str = None) -> List[Dict[str, Any]]:
        """Performs linear scan cosine similarity search filtered by chat_id."""
        scores = []
        for doc in self.knowledge_base:
            if doc.get("chat_id") == chat_id and doc.get("embedding_model") == (embedding_model or self.embedding_model):
                score = cosine_similarity(query_embedding, doc["embedding"])
                scores.append((score, doc))
        scores.sort(reverse=True, key=lambda x: x[0])
        return [doc for score, doc in scores[:limit]]

    def delete_chat(self, chat_id: str) -> None:
        """Removes all documents belonging to the specified chat_id."""
        self.knowledge_base = [doc for doc in self.knowledge_base if doc.get("chat_id") != chat_id]
        if os.path.exists(self.db_path):
            self.save()
        self._delete_from_other_indexes(chat_id)

    def delete_document(self, chat_id: str, source_file: str) -> None:
        self.knowledge_base = [
            row for row in self.knowledge_base
            if not (row.get("chat_id") == chat_id and row.get("source_file") == source_file
                    and row.get("embedding_model") == self.embedding_model)
        ]
        self.save()
        self._delete_from_other_indexes(chat_id, source_file)

    def _delete_from_other_indexes(self, chat_id: str, source_file: str = None) -> None:
        """Remove scoped records from other model-specific local indexes too."""
        current_path = os.path.abspath(self.db_path)
        for path in glob.glob("./simple_vector_db_*.json") + ["./simple_vector_db.json"]:
            if os.path.abspath(path) == current_path:
                continue
            try:
                with open(path, "r", encoding="utf-8") as source:
                    rows = json.load(source)
                kept = [
                    row for row in rows
                    if not (row.get("chat_id") == chat_id and (source_file is None or row.get("source_file") == source_file))
                ]
                if len(kept) != len(rows):
                    with open(path, "w", encoding="utf-8") as destination:
                        json.dump(kept, destination)
            except (OSError, ValueError, TypeError):
                continue

    def list_indexed_documents(self, chat_id: str) -> set:
        return {
            row.get("source_file") for row in self.knowledge_base
            if row.get("chat_id") == chat_id and row.get("embedding_model") == self.embedding_model
            and row.get("source_file")
        }

    def clear(self) -> None:
        """Wipes the local vector indexes across embedding models."""
        self.knowledge_base = []
        for path in set(glob.glob("./simple_vector_db_*.json") + [self.db_path, "./simple_vector_db.json"]):
            if not os.path.exists(path):
                continue
            try:
                os.remove(path)
            except Exception:
                pass
