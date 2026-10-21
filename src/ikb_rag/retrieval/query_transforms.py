"""Query transformation module for intent routing and query decomposition.

Classifies incoming queries as SIMPLE or COMPLEX and decomposes complex queries
into targeted sub-queries for multi-angle vector retrieval.
"""

import json
from typing import List, Tuple
from src.ikb_rag.generation.llm_client import GroqClient
from src.ikb_rag.generation.prompt_templates import ROUTER_PROMPT_TEMPLATE, DECOMPOSER_PROMPT_TEMPLATE


class QueryTransformer:
    """Handles query intent classification and complex query decomposition."""

    def __init__(self, llm_client: GroqClient):
        self.llm_client = llm_client

    def classify_intent(self, question: str) -> str:
        """Classifies the query intent as either 'SIMPLE' or 'COMPLEX'."""
        print(f"\n[AGENT] Analyzing query intent for: '{question}'")
        router_prompt = ROUTER_PROMPT_TEMPLATE.format(question=question)
        router_response = self.llm_client.generate(router_prompt, json_mode=True)

        intent = "SIMPLE"
        try:
            if router_response:
                intent = json.loads(router_response).get("intent", "SIMPLE")
        except Exception:
            pass

        print(f"[AGENT] Routing Decision: {intent}")
        return intent

    def decompose_query(self, question: str) -> List[str]:
        """Decomposes a complex question into 2-4 focused sub-queries."""
        print("[AGENT] Triggering QA Decomposer...")
        decomp_prompt = DECOMPOSER_PROMPT_TEMPLATE.format(question=question)
        decomp_response = self.llm_client.generate(decomp_prompt, json_mode=True)

        sub_queries = [question]
        try:
            if decomp_response:
                sub_queries = json.loads(decomp_response).get("sub_queries", [question])
        except Exception:
            pass

        print(f"[AGENT] Decomposed into {len(sub_queries)} sub-queries: {sub_queries}")
        return sub_queries
