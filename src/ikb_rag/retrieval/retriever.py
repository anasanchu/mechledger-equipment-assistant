"""Vector retrieval and parent-document context assembly module.

Executes vector similarity search across Qdrant Cloud or local JSON fallback,
and deduplicates results to construct rich parent-document context blocks.
"""

from typing import List, Dict, Any, Union
from src.ikb_rag.embeddings.embedder import NomicEmbedder
from src.ikb_rag.vectorstore.qdrant_store import QdrantStore
from src.ikb_rag.vectorstore.simple_json_store import SimpleJsonStore


class Retriever:
    """Manages semantic search and parent-document context construction."""

    def __init__(self, embedder: NomicEmbedder, store: Union[QdrantStore, SimpleJsonStore]):
        self.embedder = embedder
        self.store = store

    def retrieve_context(self, q_str: str, chat_id: str, limit: int = 6) -> List[Dict[str, Any]]:
        """Returns raw payload dictionaries from the active vector store for a query string."""
        emb_result = self.embedder.get_embeddings([q_str], task_type="search_query")
        if isinstance(emb_result, dict) and "error" in emb_result:
            print(f"Nomic API Error: {emb_result['error']}")
            return []

        q_emb = emb_result[0]
        return self.store.search(q_emb, chat_id=chat_id, limit=limit)

    def assemble_context(self, all_payloads: List[Dict[str, Any]]) -> str:
        """Groups payloads by page_id and constructs an optimized multi-source context string."""
        grouped_pages = {}
        for payload in all_payloads:
            # Fallback for legacy data structures if database hasn't been cleared
            page_id = payload.get("page_id", payload.get("text", ""))

            if page_id not in grouped_pages:
                grouped_pages[page_id] = {
                    "source": payload.get("source_file", "Unknown"),
                    "page_num": payload.get("page_num", "?"),
                    "link": payload.get("link", ""),
                    "parent_context": payload.get("parent_context", ""),
                    "matched_elements": [payload.get("matched_element", payload.get("text", ""))]
                }
            else:
                element = payload.get("matched_element", payload.get("text", ""))
                if element not in grouped_pages[page_id]["matched_elements"]:
                    grouped_pages[page_id]["matched_elements"].append(element)

        # Build optimized context string
        context_blocks = []
        for page_data in grouped_pages.values():
            block = f"[Source: {page_data['source']}, Page: {page_data['page_num']}, Link: {page_data['link']}]\n"
            block += "Specific Elements Matched by Search:\n"
            for el in page_data["matched_elements"]:
                block += f"- {el}\n"
            if page_data['parent_context']:
                block += f"\nFull Page Context for RCA/Troubleshooting:\n{page_data['parent_context']}"
            context_blocks.append(block)

        return "\n\n====================\n\n".join(context_blocks)
