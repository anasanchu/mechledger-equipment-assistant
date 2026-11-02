"""Response generation module combining retrieved context and Groq LLM synthesis.

Applies context character caps, prompt formatting, and sampling parameters.
"""

from typing import Optional
from src.ikb_rag.generation.llm_client import GroqClient
from src.ikb_rag.generation.prompt_templates import INDUSTRIAL_COPILOT_PROMPT_TEMPLATE


class ResponseGenerator:
    """Formats prompt with context and synthesizes final answer via LLM."""

    def __init__(self, llm_client: GroqClient):
        self.llm_client = llm_client

    def generate_response(self, question: str, context: str) -> str:
        """Formats context with prompt and calls Groq to generate industrial troubleshooting advice.
        
        Args:
            question: User's original question.
            context: Deduplicated, formatted context string from retriever.
            
        Returns:
            Synthesized answer or fallback error message.
        """
        if not context.strip():
            return (
                "## Evidence not found\n\nNo indexed document passage matched this question in the current case. "
                "I cannot establish a cause or recommend a document-based procedure from the available evidence. "
                "Add the relevant equipment manual or provide the missing equipment and operating details, then retry.\n\n"
                "**Safety:** Follow your site's approved procedures and the current manufacturer instructions."
            )

        if len(context) > 15000:
            context = context[:15000] + "\n\n...[Context Truncated to prevent Rate Limits]..."

        prompt = INDUSTRIAL_COPILOT_PROMPT_TEMPLATE.format(context=context, question=question)

        print("[AGENT] Synthesizing final response via Groq...")
        return self.llm_client.generate(prompt, temperature=0.3) or "Error generating response."
