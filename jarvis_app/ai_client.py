import json
from typing import Optional

import requests

from jarvis_app.config import DEFAULT_MODEL, OPENAI_BASE_URL, get_api_key


class AIClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or get_api_key()
        self.model = DEFAULT_MODEL

    def ask(self, prompt: str) -> str:
        if not self.api_key:
            return ""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are Jarvis, a helpful desktop assistant. Keep responses concise, friendly, and practical."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
        }

        try:
            response = requests.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(payload),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return ""
