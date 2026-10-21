"""Standard library unittest for individual pipeline components."""

import unittest
import tempfile
import os
from src.ikb_rag.vectorstore.simple_json_store import cosine_similarity, SimpleJsonStore
from src.ikb_rag.ingestion.chunking import StructuralElementChunker


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


if __name__ == "__main__":
    unittest.main()
