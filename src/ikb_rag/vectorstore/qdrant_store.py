"""Qdrant Cloud vector store integration.

Manages collection lifecycle, vector upsertion, and filtered nearest-neighbor queries.
"""

import uuid
from typing import List, Dict, Any, Optional
from config.settings import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, VECTOR_DIMENSION, OLLAMA_EMBED_MODEL


class QdrantStore:
    """Wrapper around QdrantClient for vector indexing and retrieval."""

    def __init__(self, url: str = None, api_key: str = None, collection_name: str = None):
        self.url = url or QDRANT_URL
        self.api_key = api_key or QDRANT_API_KEY
        self.collection_name = collection_name or QDRANT_COLLECTION_NAME
        self.embedding_model = OLLAMA_EMBED_MODEL
        self.client = None
        self._initialize()

    def _initialize(self) -> None:
        """Connects to Qdrant Cloud and verifies/creates the target collection."""
        from qdrant_client import QdrantClient
        from qdrant_client.http.models import Distance, VectorParams

        self.client = QdrantClient(
            url=self.url,
            api_key=self.api_key,
            check_compatibility=False,
            timeout=5.0
        )
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=VECTOR_DIMENSION, distance=Distance.COSINE),
            )
        else:
            config = self.client.get_collection(self.collection_name).config.params.vectors
            size = getattr(config, "size", None)
            if size != VECTOR_DIMENSION:
                raise ValueError(
                    f"Qdrant collection '{self.collection_name}' has vector dimension {size}; "
                    f"Ollama model '{OLLAMA_EMBED_MODEL}' is configured for {VECTOR_DIMENSION}. "
                    "Choose a new collection name and re-index the source PDFs; existing vectors were not changed."
                )

    def add_documents(self, payloads: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        """Upserts embedded vectors along with their metadata payloads."""
        from qdrant_client.http.models import PointStruct

        points = []
        for i, emb in enumerate(embeddings):
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload={**payloads[i], "embedding_model": self.embedding_model}
            ))
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_embedding: List[float], chat_id: str, limit: int = 6, embedding_model: str = None) -> List[Dict[str, Any]]:
        """Queries Qdrant with a vector embedding filtered by chat_id."""
        from qdrant_client.http.models import Filter, FieldCondition, MatchValue

        conditions = [FieldCondition(key="chat_id", match=MatchValue(value=chat_id))]
        model = embedding_model or self.embedding_model
        conditions.append(FieldCondition(key="embedding_model", match=MatchValue(value=model)))
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=Filter(must=conditions),
            limit=limit
        )
        return [hit.payload for hit in search_result.points]

    def delete_chat(self, chat_id: str) -> None:
        """Deletes all indexed points for a given chat_id."""
        from qdrant_client.http.models import Filter, FieldCondition, MatchValue

        try:
            selector = Filter(must=[FieldCondition(key="chat_id", match=MatchValue(value=chat_id))])
            for collection in self._owned_model_collections():
                self.client.delete(collection_name=collection, points_selector=selector)
        except Exception as e:
            print(f"[WARNING] Qdrant deletion failed (Index may not exist yet): {e}")

    def delete_document(self, chat_id: str, source_file: str) -> None:
        from qdrant_client.http.models import Filter, FieldCondition, MatchValue
        selector = Filter(must=[
            FieldCondition(key="chat_id", match=MatchValue(value=chat_id)),
            FieldCondition(key="source_file", match=MatchValue(value=source_file)),
        ])
        for collection in self._owned_model_collections():
            self.client.delete(collection_name=collection, points_selector=selector)

    def _owned_model_collections(self) -> List[str]:
        """Find app-owned model indexes so scoped deletion covers prior models."""
        names = [item.name for item in self.client.get_collections().collections]
        managed = {name for name in names if name.startswith("mechledger-") or name == "nomic-manual"}
        return sorted({self.collection_name, *managed}.intersection(names))

    def list_indexed_documents(self, chat_id: str) -> set:
        from qdrant_client.http.models import Filter, FieldCondition, MatchValue
        source_names, offset = set(), None
        query_filter = Filter(must=[
            FieldCondition(key="chat_id", match=MatchValue(value=chat_id)),
            FieldCondition(key="embedding_model", match=MatchValue(value=self.embedding_model)),
        ])
        while True:
            points, offset = self.client.scroll(
                collection_name=self.collection_name, scroll_filter=query_filter,
                limit=256, offset=offset, with_payload=["source_file"], with_vectors=False,
            )
            source_names.update(point.payload.get("source_file") for point in points if point.payload and point.payload.get("source_file"))
            if offset is None:
                break
        return source_names

    def clear(self) -> None:
        """Deletes MECHLEDGER model collections and recreates the active one."""
        from qdrant_client.http.models import Distance, VectorParams
        try:
            for collection in self._owned_model_collections():
                self.client.delete_collection(collection_name=collection)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=VECTOR_DIMENSION, distance=Distance.COSINE),
            )
        except Exception:
            pass
