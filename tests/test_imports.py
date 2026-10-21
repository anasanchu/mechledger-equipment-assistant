"""Standard library unittest for imports and module resolution."""

import unittest


class TestImports(unittest.TestCase):

    def test_import_config(self):
        import config
        from config.settings import GROQ_MODEL, NOMIC_EMBED_MODEL, API_PORT
        self.assertIn(GROQ_MODEL, ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b", "llama-3.3-70b-versatile"])
        self.assertEqual(NOMIC_EMBED_MODEL, "nomic-embed-text-v1.5")
        self.assertEqual(API_PORT, 8002)

    def test_import_vectorstore(self):
        from src.ikb_rag.vectorstore.simple_json_store import cosine_similarity, SimpleJsonStore
        v1 = [1.0, 0.0]
        v2 = [1.0, 0.0]
        self.assertEqual(cosine_similarity(v1, v2), 1.0)

    def test_import_generation(self):
        from src.ikb_rag.generation.prompt_templates import (
            ROUTER_PROMPT_TEMPLATE,
            DECOMPOSER_PROMPT_TEMPLATE,
            INDUSTRIAL_COPILOT_PROMPT_TEMPLATE,
        )
        self.assertIn("{question}", ROUTER_PROMPT_TEMPLATE)
        self.assertIn("{question}", DECOMPOSER_PROMPT_TEMPLATE)
        self.assertIn("{context}", INDUSTRIAL_COPILOT_PROMPT_TEMPLATE)

    def test_import_api_schemas(self):
        from api.schemas import (
            QueryRequest,
            QueryResponse,
            UploadResponse,
            DocumentListResponse,
            MessageResponse,
        )
        req = QueryRequest(question="What is pump cavitation?")
        self.assertEqual(req.question, "What is pump cavitation?")
        self.assertEqual(req.chat_id, "default")
        
        q_res = QueryResponse(answer="Check impeller.")
        self.assertEqual(q_res.answer, "Check impeller.")

        u_res = UploadResponse(message="Indexed", filename="manual.pdf")
        self.assertEqual(u_res.filename, "manual.pdf")

        d_res = DocumentListResponse(documents=["manual.pdf"])
        self.assertEqual(len(d_res.documents), 1)

        m_res = MessageResponse(message="Success")
        self.assertEqual(m_res.message, "Success")

    def test_import_api_app(self):
        from api.main import app
        self.assertEqual(app.title, "IKB-RAG API")

    def test_ikb_rag_root_import(self):
        from src.ikb_rag import IKBRagEngine, rag_engine
        self.assertIsNotNone(rag_engine)
        self.assertTrue(callable(IKBRagEngine))


if __name__ == "__main__":
    unittest.main()
