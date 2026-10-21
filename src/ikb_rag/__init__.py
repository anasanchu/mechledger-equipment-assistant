"""IKB-RAG root package.

Exposes the primary IKBRagEngine class and singleton instance rag_engine.
"""

from .pipeline.rag_pipeline import IKBRagEngine, rag_engine

__all__ = ["IKBRagEngine", "rag_engine"]
