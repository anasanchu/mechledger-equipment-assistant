"""Standard library unittest for individual pipeline components."""

import unittest
import tempfile
import os
from unittest.mock import patch, Mock
from src.ikb_rag.vectorstore.simple_json_store import cosine_similarity, SimpleJsonStore
from src.ikb_rag.ingestion.chunking import StructuralElementChunker
from src.ikb_rag.embeddings.embedder import NomicEmbedder
from api.reporting import build_report_pdf


class TestComponents(unittest.TestCase):

    def test_cosine_similarity_orthogonal(self):
        v1 = [1.0, 0.0]
        v2 = [0.0, 1.0]
        self.assertEqual(cosine_similarity(v1, v2), 0.0)

    def test_cosine_similarity_zero_magnitude(self):
        v1 = [0.0, 0.0]
        v2 = [1.0, 1.0]
        self.assertEqual(cosine_similarity(v1, v2), 0.0)

    def test_simple_json_store(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_db = os.path.join(tmp_dir, "test_db.json")
            store = SimpleJsonStore(db_path=test_db)

            payloads = [{"chat_id": "test_chat", "page_id": "p1", "text": "sample text"}]
            embeddings = [[1.0, 0.0, 0.0]]
            store.add_documents(payloads, embeddings)

            results = store.search([1.0, 0.0, 0.0], chat_id="test_chat", limit=1)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["page_id"], "p1")

            # Test delete
            store.delete_chat("test_chat")
            results = store.search([1.0, 0.0, 0.0], chat_id="test_chat", limit=1)
            self.assertEqual(len(results), 0)

    def test_json_store_separates_embedding_models(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SimpleJsonStore(db_path=os.path.join(tmp_dir, "model_index.json"))
            store.add_documents(
                [{"chat_id": "isolated", "source_file": "manual.pdf"}], [[1.0, 0.0]]
            )
            other_model = store.knowledge_base[0].copy()
            other_model["embedding_model"] = "different-model"
            other_model["embedding"] = [0.0, 1.0]
            store.knowledge_base.append(other_model)
            self.assertEqual(len(store.search([1.0, 0.0], "isolated")), 1)

    def test_chunking_fallback(self):
        chunker = StructuralElementChunker(api_port=8002)
        raw, payloads = chunker.chunk(
            parsed_data={},
            text="A" * 3200,
            chat_id="c1",
            base_name="manual.pdf",
            pdf_base="manual",
            doc_url="http://localhost:8002/documents/c1/manual.pdf"
        )
        self.assertEqual(len(raw), 3)
        self.assertEqual(len(payloads), 3)
        self.assertEqual(payloads[0]["source_file"], "manual.pdf")

    @patch("src.ikb_rag.embeddings.embedder.requests.post")
    def test_ollama_embeddings_batch_and_dimension(self, post):
        post.return_value = Mock(status_code=200, json=lambda: {"embeddings": [[0.0] * 768, [1.0] * 768]})
        post.return_value.raise_for_status.return_value = None
        result = NomicEmbedder().get_embeddings(["one", "two"])
        self.assertEqual(len(result), 2)
        self.assertEqual(post.call_args.kwargs["json"]["input"], ["search_document: one", "search_document: two"])

    @patch("src.ikb_rag.embeddings.embedder.requests.post")
    def test_ollama_rejects_incompatible_dimension(self, post):
        post.return_value = Mock(status_code=200, json=lambda: {"embeddings": [[1.0, 2.0]]})
        post.return_value.raise_for_status.return_value = None
        result = NomicEmbedder().get_embeddings(["one"])
        self.assertIn("error", result)
        self.assertIn("dimension", result["error"])

    def test_report_pdf_contains_valid_structure(self):
        pdf = build_report_pdf({"case_title": "Pump", "problem": "No flow", "documents": ["manual.pdf"]})
        self.assertTrue(pdf.startswith(b"%PDF-1.4"))
        self.assertIn(b"startxref", pdf)
        self.assertIn(b"manual.pdf", pdf)


if __name__ == "__main__":
    unittest.main()
