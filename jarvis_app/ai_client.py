import json
from typing import Optional

import requests

from jarvis_app.config import CODING_MODEL, DEFAULT_MODEL, OPENAI_BASE_URL, get_api_key


class AIClient:
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or get_api_key()
        self.model = model
        self.base_url = OPENAI_BASE_URL

    def ask(self, prompt: str, system_prompt: str = None) -> str:
        if not self.api_key:
            return ""

        default_system = "You are Jarvis, a helpful desktop assistant. Keep responses concise, friendly, and practical."
        system_content = system_prompt or default_system

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4 if self.model == DEFAULT_MODEL else 0.3,
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=45,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return ""

    def code_review(self, code: str, language: str = "python") -> str:
        """Get AI review and suggestions for code."""
        system = f"You are an expert {language} code reviewer. Provide concise, actionable feedback on code quality, performance, security, and best practices. Be direct and helpful."
        prompt = f"Review this {language} code and suggest improvements:\n\n{code}"
        return self.ask(prompt, system_prompt=system)

    def generate_code(self, description: str, language: str = "python") -> str:
        """Generate code from a description."""
        coding_client = AIClient(api_key=self.api_key, model=CODING_MODEL)
        system = f"You are an expert {language} programmer. Generate clean, well-documented, production-ready code. Always include error handling and comments."
        prompt = f"Generate {language} code for: {description}"
        return coding_client.ask(prompt, system_prompt=system)

    def debug_error(self, error: str, context: str = "") -> str:
        """Help debug errors and provide solutions."""
        system = "You are a debugging expert. Analyze errors, identify root causes, and provide clear solutions."
        prompt = f"Error: {error}\n\nContext: {context}\n\nHelp me debug this."
        return self.ask(prompt, system_prompt=system)

    def explain_code(self, code: str) -> str:
        """Explain what code does."""
        system = "You are a code explanation expert. Explain code clearly and concisely, breaking down complex logic."
        prompt = f"Explain this code:\n\n{code}"
        return self.ask(prompt, system_prompt=system)
