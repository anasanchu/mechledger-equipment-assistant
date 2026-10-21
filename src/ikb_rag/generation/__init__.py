"""Generation package for prompts, LLM client, and response synthesis."""

from .prompt_templates import (
    ROUTER_PROMPT_TEMPLATE,
    DECOMPOSER_PROMPT_TEMPLATE,
    INDUSTRIAL_COPILOT_PROMPT_TEMPLATE,
)
from .llm_client import GroqClient
from .response_generator import ResponseGenerator
