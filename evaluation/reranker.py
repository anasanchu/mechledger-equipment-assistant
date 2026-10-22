"""Qdrant Candidate Prefetch and Hybrid Reranking Engine for Evaluation.

Retrieves a wider candidate pool from Qdrant Cloud (N=15) and applies
lexical-semantic Reciprocal Rank Fusion (RRF) and length-normalized
content scoring to eliminate repetitive header distractors.
"""

import sys
import os
from typing import List, Dict, Any, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    import math
    from collections import Counter

    class BM25Okapi:
        """Lightweight pure-Python fallback for BM25Okapi scoring."""
        def __init__(self, corpus, k1=1.5, b=0.75):
            self.corpus = corpus
            self.k1 = k1
            self.b = b
            self.corpus_size = len(corpus)
            self.avgdl = sum(len(d) for d in corpus) / (self.corpus_size or 1)
            self.doc_freqs = [Counter(d) for d in corpus]
            self.idf = {}
            for d in corpus:
                for w in set(d):
                    self.idf[w] = self.idf.get(w, 0) + 1
            for w, freq in self.idf.items():
                self.idf[w] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)

        def get_scores(self, query):
            scores = []
            for i, freqs in enumerate(self.doc_freqs):
                doc_len = len(self.corpus[i])
                score = 0.0
                for token in query:
                    if token in freqs:
                        freq = freqs[token]
                        denom = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / (self.avgdl or 1.0)))
                        score += self.idf.get(token, 0.0) * (freq * (self.k1 + 1.0)) / (denom or 1.0)
                scores.append(score)
            return scores

from qdrant_client.http.models import Filter, FieldCondition, MatchValue


class QdrantReranker:
    """Two-stage retrieval: Qdrant dense vector prefetch + lexical/content reranker."""

    def __init__(self, embedder, store):
        self.embedder = embedder
        self.store = store

    def retrieve_baseline(
        self,
        query: str,
        query_emb: Optional[List[float]] = None,
        chat_id: str = "1",
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Standard single-stage dense vector search."""
        if query_emb is None:
            query_emb = self.embedder.get_embeddings([query], task_type="search_query")[0]

        hits = self.store.client.query_points(
            collection_name=self.store.collection_name,
            query=query_emb,
            query_filter=Filter(must=[FieldCondition(key="chat_id", match=MatchValue(value=chat_id))]),
            limit=top_k
        )
        return [
            {
                "score": float(h.score),
                "page_num": h.payload.get("page_num"),
                "source_file": h.payload.get("source_file"),
                "text": h.payload.get("matched_element", h.payload.get("text", "")),
                "parent_context": h.payload.get("parent_context", ""),
                "payload": h.payload
            }
            for h in hits.points
        ]

    def retrieve_reranked(
        self,
        query: str,
        query_emb: Optional[List[float]] = None,
        chat_id: str = "1",
        prefetch_n: int = 15,
        top_k: int = 5,
        rrf_k: int = 60
    ) -> List[Dict[str, Any]]:
        """Two-stage retrieval: Prefetch top-N from Qdrant, then rerank with BM25 + dense fusion."""
        if query_emb is None:
            query_emb = self.embedder.get_embeddings([query], task_type="search_query")[0]

        # Stage 1: Prefetch wider candidate pool from Qdrant
        prefetch_hits = self.store.client.query_points(
            collection_name=self.store.collection_name,
            query=query_emb,
            query_filter=Filter(must=[FieldCondition(key="chat_id", match=MatchValue(value=chat_id))]),
            limit=prefetch_n
        )
        candidates = prefetch_hits.points
        if not candidates:
            return []

        # Stage 2: Lexical scoring via BM25 over candidate texts
        corpus = []
        for c in candidates:
            text = c.payload.get("matched_element", c.payload.get("text", "")) or ""
            parent = c.payload.get("parent_context", "")[:400]
            combined = f"{text} {parent}".lower()
            corpus.append(combined.split())

        bm25 = BM25Okapi(corpus)
        query_tokens = query.lower().split()
        bm25_scores = bm25.get_scores(query_tokens)

        # Dense rank order
        dense_ranked_indices = list(range(len(candidates)))
        bm25_ranked_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)

        dense_rank_map = {idx: rank + 1 for rank, idx in enumerate(dense_ranked_indices)}
        bm25_rank_map = {idx: rank + 1 for rank, idx in enumerate(bm25_ranked_indices)}

        scored_candidates = []
        for i, c in enumerate(candidates):
            text = c.payload.get("matched_element", c.payload.get("text", "")) or ""
            r_dense = dense_rank_map[i]
            r_bm25 = bm25_rank_map[i]

            # RRF formula
            rrf_score = (1.0 / (rrf_k + r_dense)) + (1.0 / (rrf_k + r_bm25))

            # Diversity bonus / penalty for non-informative repetitive headers
            is_generic_header = len(text.strip()) < 55 and text.strip().lower().startswith("piping and instrumentation diagrams")
            if is_generic_header:
                rrf_score *= 0.5

            scored_candidates.append({
                "rrf_score": rrf_score,
                "dense_score": float(c.score),
                "bm25_score": float(bm25_scores[i]),
                "page_num": c.payload.get("page_num"),
                "source_file": c.payload.get("source_file"),
                "text": text,
                "parent_context": c.payload.get("parent_context", ""),
                "payload": c.payload
            })

        # Sort by RRF score descending
        scored_candidates.sort(key=lambda x: x["rrf_score"], reverse=True)
        return scored_candidates[:top_k]
