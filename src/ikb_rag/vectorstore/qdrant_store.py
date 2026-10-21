"""Qdrant Cloud vector store integration.

Manages collection lifecycle, vector upsertion, and filtered nearest-neighbor queries.
"""

import uuid
from typing import List, Dict, Any, Optional
from config.settings import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, VECTOR_DIMENSION


class QdrantStore:
    """Wrapper around QdrantClient for vector indexing and retrieval."""

    def __init__(self, url: str = None, api_key: str = None, collection_name: str = None):
        self.url = url or QDRANT_URL
        self.api_key = api_key or QDRANT_API_KEY
        self.collection_name = collection_name or QDRANT_COLLECTION_NAME
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

    def add_documents(self, payloads: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        """Upserts embedded vectors along with their metadata payloads."""
        from qdrant_client.http.models import PointStruct

        points = []
        for i, emb in enumerate(embeddings):
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload=payloads[i]
            ))
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_embedding: List[float], chat_id: str, limit: int = 6) -> List[Dict[str, Any]]:
        """Queries Qdrant with a vector embedding filtered by chat_id."""
        from qdrant_client.http.models import Filter, FieldCondition, MatchValue

        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=Filter(must=[FieldCondition(key="chat_id", match=MatchValue(value=chat_id))]),
            limit=limit
        )
        return [hit.payload for hit in search_result.points]

    def delete_chat(self, chat_id: str) -> None:
        """Deletes all indexed points for a given chat_id."""
        from qdrant_client.http.models import Filter, FieldCondition, MatchValue

        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[FieldCondition(key="chat_id", match=MatchValue(value=chat_id))]
                )
            )
        except Exception as e:
            print(f"[WARNING] Qdrant deletion failed (Index may not exist yet): {e}")

    def clear(self) -> None:
        """Deletes the entire collection from Qdrant Cloud."""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
        except Exception:
            pass
