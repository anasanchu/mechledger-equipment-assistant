"""MECHLEDGER RAG pipeline orchestrator.

Coordinates ingestion, vector storage, query transformation, retrieval,
and response generation. Preserves exact engine behaviors and public interfaces.
"""

import os
from typing import Optional, List, Dict, Any

from config.settings import (
    HF_TOKEN,
    GROQ_API_KEY,
    QDRANT_URL,
    QDRANT_API_KEY,
    DB_PATH,
    QDRANT_COLLECTION_NAME,
    OLLAMA_CHAT_MODEL,
)
from src.ikb_rag.embeddings.embedder import NomicEmbedder
from src.ikb_rag.vectorstore.qdrant_store import QdrantStore
from src.ikb_rag.vectorstore.simple_json_store import SimpleJsonStore
from src.ikb_rag.vectorstore.index_manager import IndexManager
from src.ikb_rag.ingestion.loaders import MinerUDocumentLoader
from src.ikb_rag.ingestion.chunking import StructuralElementChunker
from src.ikb_rag.generation.llm_client import GroqClient
from src.ikb_rag.generation.response_generator import ResponseGenerator
from src.ikb_rag.retrieval.query_transforms import QueryTransformer
from src.ikb_rag.retrieval.retriever import Retriever


class IKBRagEngine:
    """Core RAG engine managing document ingestion, semantic search, and troubleshooting synthesis."""

    def __init__(self):
        print("\n" + "=" * 50)
        print("[*] INITIALIZING MECHLEDGER ENGINE")
        print("=" * 50)

        self.hf_token = HF_TOKEN
        self.groq_api_key = GROQ_API_KEY

        # 1. Check Groq LLM Connection
        if self.groq_api_key:
            print("[SUCCESS] Groq API Key found (LLM Inference Ready)")
        else:
            print(f"[INFO] Groq key missing. Chat will use local Ollama model: {OLLAMA_CHAT_MODEL}.")

        # 2. Check Qdrant Cloud DB Connection
        self.qdrant_url = QDRANT_URL
        self.qdrant_api_key = QDRANT_API_KEY
        self.use_qdrant = bool(self.qdrant_url and self.qdrant_api_key)

        self.db_path = DB_PATH
        self.collection_name = QDRANT_COLLECTION_NAME

        if self.use_qdrant:
            try:
                self.qdrant_store = QdrantStore(
                    url=self.qdrant_url,
                    api_key=self.qdrant_api_key,
                    collection_name=self.collection_name
                )
                self.qdrant = self.qdrant_store.client
                self.active_store = self.qdrant_store
                print("[SUCCESS] Qdrant Cloud connected successfully!")
            except Exception as e:
                print(f"[ERROR] Qdrant Connection Failed: {e}")
                self.use_qdrant = False

        if not self.use_qdrant:
            print(f"[WARNING] Qdrant unavailable. Falling back to {self.db_path}")
            self.json_store = SimpleJsonStore(db_path=self.db_path)
            self.active_store = self.json_store

        # 3. Local Ollama embedding configuration
        print("[INFO] Technical embeddings are generated locally through Ollama.")

        print("[SUCCESS] MinerU API configured for document processing.")
        print("=" * 50 + "\n")

        # Initialize modular sub-components
        self.embedder = NomicEmbedder()
        self.llm_client = GroqClient(api_key=self.groq_api_key)
        self.loader = MinerUDocumentLoader(hf_token=self.hf_token)
        self.chunker = StructuralElementChunker()
        self.retriever = Retriever(embedder=self.embedder, store=self.active_store)
        self.transformer = QueryTransformer(llm_client=self.llm_client)
        self.generator = ResponseGenerator(llm_client=self.llm_client)
        self.index_manager = IndexManager(store=self.active_store)

    @property
    def knowledge_base(self):
        """Maintains backward compatibility with direct knowledge_base attribute access."""
        if hasattr(self, "json_store"):
            return self.json_store.knowledge_base
        return []

    @knowledge_base.setter
    def knowledge_base(self, value):
        if hasattr(self, "json_store"):
            self.json_store.knowledge_base = value

    def _get_embeddings(self, texts, task_type="search_document"):
        """Backward-compatibility internal method alias."""
        return self.embedder.get_embeddings(texts, task_type=task_type)

    def _call_groq(self, prompt: str, temperature=0.1, json_mode=False):
        """Backward-compatibility internal method alias."""
        return self.llm_client.generate(prompt, temperature=temperature, json_mode=json_mode)

    def _retrieve_context(self, q_str: str, chat_id: str, limit: int = 6):
        """Backward-compatibility internal method alias."""
        return self.retriever.retrieve_context(q_str, chat_id, limit=limit)

    def index_document(self, file_path: str, chat_id: str = "default") -> int:
        """Loads, parses, chunks, and indexes an industrial document into the vector store."""
        parsed_data, text, base_name, pdf_base, doc_url = self.loader.load_and_parse(file_path, chat_id)
        raw_elements, payloads = self.chunker.chunk(parsed_data, text, chat_id, base_name, pdf_base, doc_url)

        print("🟡 Queue: Generating vector embeddings...")
        embeddings = self.embedder.get_embeddings(raw_elements, task_type="search_document")

        if isinstance(embeddings, dict) and "error" in embeddings:
            raise RuntimeError(f"Ollama embedding error: {embeddings['error']}")

        # Replace vectors for this source only after extraction and embedding
        # succeeded, so refresh attempts preserve the previous index on failure.
        self.active_store.delete_document(chat_id, base_name)
        print(f"Indexing {len(raw_elements)} chunks into Vector DB...")
        self.active_store.add_documents(payloads, embeddings)

        if self.use_qdrant:
            print("🟢 Done: Saved to Qdrant Cloud!")
        else:
            print("🟢 Done: Saved to local JSON DB!")

        print("=" * 50 + "\n")
        return len(raw_elements)

    def refresh_chat_data(self, chat_id: str) -> str:
        """Re-indexes all documents belonging to a chat_id."""
        return self.index_manager.refresh_chat_data(chat_id, self.index_document)

    def delete_chat_data(self, chat_id: str) -> str:
        """Purges vectors and cached documents for a chat_id."""
        return self.index_manager.delete_chat_data(chat_id)

    def clear_knowledge_base(self) -> str:
        """Erases all vectors and cleared storage folders."""
        return self.index_manager.clear_knowledge_base()

    def query(self, question: str, chat_id: str = "default") -> str:
        """End-to-end question answering pipeline with query decomposition and RCA synthesis."""
        intent = self.transformer.classify_intent(question)

        all_payloads = []
        if intent == "COMPLEX":
            sub_queries = self.transformer.decompose_query(question)
            for sub_q in sub_queries:
                payloads = self.retriever.retrieve_context(sub_q, chat_id, limit=3)
                all_payloads.extend(payloads)
        else:
            all_payloads = self.retriever.retrieve_context(question, chat_id, limit=6)

        context = self.retriever.assemble_context(all_payloads)
        return self.generator.generate_response(question, context)


# Singleton instance
rag_engine = IKBRagEngine()
