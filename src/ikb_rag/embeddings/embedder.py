"""Nomic Atlas embedding model wrapper.

Interacts with the Nomic embedding API to generate dense vector embeddings
for text chunks and user queries.
"""

import requests
from typing import List, Union, Dict, Any
from config.settings import NOMIC_API_KEY, NOMIC_API_URL, NOMIC_EMBED_MODEL


class NomicEmbedder:
    """Client for generating embeddings using the Nomic Atlas API."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or NOMIC_API_KEY

    def get_embeddings(
        self, texts: List[str], task_type: str = "search_document"
    ) -> Union[List[List[float]], Dict[str, Any]]:
        """Generates embeddings for a list of texts using Nomic embed API.
        
        Args:
            texts: List of text strings to embed.
            task_type: Task type hint ('search_document' or 'search_query').
            
        Returns:
            List of float vector embeddings or error dictionary.
        """
        if not self.api_key:
            return {"error": "Nomic API Key not provided"}

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": NOMIC_EMBED_MODEL,
                "texts": texts,
                "task_type": task_type
            }
            response = requests.post(NOMIC_API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json().get('embeddings', [])
            else:
                return {"error": f"HTTP {response.status_code} - {response.text}"}
        except Exception as e:
            print(f"Nomic API Error: {e}")
            return {"error": str(e)}
