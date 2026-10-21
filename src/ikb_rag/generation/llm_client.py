"""Groq LLM API client wrapper.

Manages chat completion requests to the Llama 3 model on Groq, supporting
standard inference and JSON-mode structured output.
"""

import requests
from typing import Optional
from config.settings import GROQ_API_KEY, GROQ_MODEL, GROQ_API_URL


class GroqClient:
    """Wrapper around the Groq OpenAI-compatible Chat Completions API."""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or GROQ_API_KEY
        self.model = model or GROQ_MODEL

    def generate(self, prompt: str, temperature: float = 0.1, json_mode: bool = False) -> Optional[str]:
        """Calls Groq API to generate response content.
        
        Args:
            prompt: Text prompt string.
            temperature: Sampling temperature (default 0.1).
            json_mode: Whether to enforce JSON object response format.
            
        Returns:
            Generated response string or None if failed.
        """
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

        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"Groq API Error: {response.text}")
            return None
