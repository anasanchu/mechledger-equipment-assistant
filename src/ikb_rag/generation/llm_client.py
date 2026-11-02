"""Groq LLM API client wrapper.

Manages chat completion requests to the Llama 3 model on Groq, supporting
standard inference and JSON-mode structured output.
"""

import requests
from typing import Optional
from config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_API_URL,
    OLLAMA_BASE_URL,
    OLLAMA_CHAT_MODEL,
)


class GroqClient:
    """Wrapper around the Groq OpenAI-compatible Chat Completions API."""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or GROQ_API_KEY
        self.model = model or GROQ_MODEL

    def _generate_locally(self, prompt: str, temperature: float, json_mode: bool):
        """Generate a response with a locally running Ollama chat model."""
        payload = {
            "model": OLLAMA_CHAT_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": temperature},
        }
        if json_mode:
            payload["format"] = "json"
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=300
            )
            response.raise_for_status()
            return response.json().get("message", {}).get("content")
        except requests.RequestException as e:
            print(f"Local Ollama error: {e}")
            print(
                "Install the local chat model with `ollama pull qwen2.5:3b`, "
                "then retry. The embedding model alone cannot answer chat questions."
            )
            return None

    def generate(self, prompt: str, temperature: float = 0.1, json_mode: bool = False) -> Optional[str]:
        """Calls Groq API to generate response content.
        
        Args:
            prompt: Text prompt string.
            temperature: Sampling temperature (default 0.1).
            json_mode: Whether to enforce JSON object response format.
            
        Returns:
            Generated response string or None if failed.
        """
        if not self.api_key:
            print("[AGENT] No Groq key configured; using local Ollama chat model.")
            return self._generate_locally(prompt, temperature, json_mode)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        if json_mode:
            data["response_format"] = {"type": "json_object"}

        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=120)
            if response.status_code in (401, 403):
                print("Groq rejected the API key; falling back to local Ollama chat model.")
                return self._generate_locally(prompt, temperature, json_mode)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.RequestException as e:
            print(f"Groq API error: {e}")
            return None
