#!/usr/bin/env python3
"""Enhanced AI client with better reasoning, memory, and specialized models."""

import json
import logging
from typing import List, Optional, Dict, Any

import requests

from jarvis_app.config import (
    OPENAI_BASE_URL,
    DEFAULT_MODEL,
    CODING_MODEL,
    ADVANCED_MODEL,
    AI_TEMPERATURE_CHAT,
    AI_TEMPERATURE_CODING,
    AI_TEMPERATURE_CREATIVE,
    AI_MAX_TOKENS,
    AI_TIMEOUT,
    get_api_key,
)

logger = logging.getLogger(__name__)


class AdvancedAIClient:
    """AI client with context memory, specialized prompts, and multi-model support."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or get_api_key()
        self.base_url = OPENAI_BASE_URL
        self.conversation_history: List[Dict[str, str]] = []
        self.context_window = 10  # Keep last 10 exchanges

    def _chat(self, messages: List[Dict[str, str]], model: str = DEFAULT_MODEL, temp: float = AI_TEMPERATURE_CHAT) -> str:
        """Internal chat call with retry logic."""
        if not self.api_key:
            return ""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temp,
                "max_tokens": AI_MAX_TOKENS,
            }
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=AI_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.exceptions.Timeout:
            return "AI request timed out. Try a simpler question."
        except requests.exceptions.RequestException as e:
            logger.error(f"AI request failed: {e}")
            return ""
        except Exception as e:
            logger.error(f"AI error: {e}")
            return ""

    def _build_messages(self, user_message: str, system_prompt: str) -> List[Dict[str, str]]:
        """Build message list with context memory."""
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation_history[-self.context_window * 2 :])
        messages.append({"role": "user", "content": user_message})
        return messages

    def ask(
        self,
        prompt: str,
        system_prompt: str = "You are Jarvis, a helpful desktop AI assistant. Keep responses clear, concise, and practical.",
    ) -> str:
        """Ask AI with context awareness."""
        messages = self._build_messages(prompt, system_prompt)
        response = self._chat(messages, model=DEFAULT_MODEL, temp=AI_TEMPERATURE_CHAT)

        if response:
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": response})

        return response

    def code_review(self, code: str) -> str:
        """Review and critique code."""
        prompt = f"""Review this code for:
1. Correctness and potential bugs
2. Performance issues
3. Best practices and style
4. Security concerns
5. Suggestions for improvement

Code:
```
{code}
```

Provide actionable feedback."""
        return self._chat(
            self._build_messages(
                prompt,
                "You are an expert code reviewer. Provide specific, actionable feedback.",
            ),
            model=CODING_MODEL,
            temp=AI_TEMPERATURE_CODING,
        )

    def generate_code(self, prompt: str, language: str = "python") -> str:
        """Generate code based on requirements."""
        full_prompt = f"""Generate clean, production-ready {language} code for:
{prompt}

Include:
- Clear comments
- Error handling
- Type hints (if applicable)
- Best practices"""
        return self._chat(
            self._build_messages(
                full_prompt,
                f"You are an expert {language} developer. Generate clean, well-documented code.",
            ),
            model=CODING_MODEL,
            temp=AI_TEMPERATURE_CODING,
        )

    def explain_code(self, code: str) -> str:
        """Explain what code does."""
        prompt = f"""Explain this code clearly:

```
{code}
```

Cover:
1. What it does overall
2. Key logic and flow
3. Any important patterns or concepts
4. How to use or modify it"""
        return self._chat(
            self._build_messages(
                prompt,
                "You are an expert at explaining code. Be clear and educational.",
            ),
            model=CODING_MODEL,
            temp=AI_TEMPERATURE_CODING,
        )

    def refactor_code(self, code: str) -> str:
        """Suggest and perform code refactoring."""
        prompt = f"""Refactor this code for readability, efficiency, and maintainability:

```
{code}
```

Provide:
1. Refactored code
2. Explanation of changes
3. Why each change improves the code"""
        return self._chat(
            self._build_messages(
                prompt,
                "You are an expert code refactorer. Improve code without changing functionality.",
            ),
            model=CODING_MODEL,
            temp=AI_TEMPERATURE_CODING,
        )

    def debug_error(self, error_message: str, code: str = "") -> str:
        """Help debug errors."""
        prompt = f"""Help me debug this error:

{error_message}

{f"Code context:\n```\n{code}\n```" if code else ""}

Provide:
1. What the error means
2. Why it happens
3. How to fix it
4. Prevention tips"""
        return self._chat(
            self._build_messages(
                prompt,
                "You are an expert debugger. Help users understand and fix errors.",
            ),
            model=CODING_MODEL,
            temp=AI_TEMPERATURE_CODING,
        )

    def creative(self, prompt: str) -> str:
        """Handle creative/open-ended requests."""
        return self._chat(
            self._build_messages(
                prompt,
                "You are a creative and thoughtful AI assistant. Help with ideas, writing, and creative thinking.",
            ),
            model=DEFAULT_MODEL,
            temp=AI_TEMPERATURE_CREATIVE,
        )

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history.clear()
