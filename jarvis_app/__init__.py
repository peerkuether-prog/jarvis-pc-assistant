import json
from typing import Optional

import requests

from jarvis_app.config import DEFAULT_MODEL, get_api_key


class AIClient:
    """Thin wrapper around the OpenAI-compatible chat completions API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or get_api_key()
        self.model = DEFAULT_MODEL

    def ask(self, prompt: str) -> str:
        if not self.api_key:
            return ""

        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful PC assistant named Jarvis. Keep responses concise, friendly, and practical."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.5,
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return ""
