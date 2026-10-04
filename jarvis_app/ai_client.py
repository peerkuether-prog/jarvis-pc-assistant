import json
import logging
from typing import Optional, List, Dict

import requests

from jarvis_app.config import (
    ADVANCED_MODEL, CODING_MODEL, DEFAULT_MODEL, OPENAI_BASE_URL, 
    AI_TEMPERATURE_CHAT, AI_TEMPERATURE_CODING, AI_TEMPERATURE_CREATIVE,
    AI_MAX_TOKENS, AI_TIMEOUT, get_log_file
)

# Setup logging
logging.basicConfig(
    filename=str(get_log_file()),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AdvancedAIClient:
    """Advanced AI client with conversation memory, reasoning, and specialization."""

    def __init__(self, api_key: Optional[str] = None):
        from jarvis_app.config import get_api_key
        self.api_key = api_key or get_api_key()
        self.base_url = OPENAI_BASE_URL
        self.conversation_history: List[Dict] = []
        self.max_history = 20

    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})
        # Keep only recent messages
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

    def _get_history_context(self) -> str:
        """Get context from conversation history."""
        if not self.conversation_history:
            return ""
        recent = self.conversation_history[-4:]
        context = "Recent context: " + " | ".join(
            f"{msg['role']}: {msg['content'][:100]}" for msg in recent
        )
        return context

    def ask(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = DEFAULT_MODEL,
        temperature: float = AI_TEMPERATURE_CHAT,
        use_history: bool = True,
    ) -> str:
        """Ask AI with advanced features."""
        if not self.api_key:
            logger.warning("No API key configured")
            return ""

        default_system = "You are Jarvis, an advanced desktop AI assistant. Be helpful, precise, and friendly."
        system_content = system_prompt or default_system
        
        # Build messages with history
        messages = [{"role": "system", "content": system_content}]
        
        if use_history and self.conversation_history:
            # Add recent context
            context = self._get_history_context()
            if context:
                messages.append({"role": "system", "content": context})
            messages.extend(self.conversation_history)
        
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": AI_MAX_TOKENS,
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=AI_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            result = data["choices"][0]["message"]["content"].strip()
            
            # Store in history
            if use_history:
                self._add_to_history("user", prompt)
                self._add_to_history("assistant", result)
            
            logger.info(f"API call successful - model: {model}")
            return result
        except requests.exceptions.Timeout:
            logger.error("API request timeout")
            return "Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return ""

    def code_review(self, code: str, language: str = "python") -> str:
        """Expert code review with detailed feedback."""
        system = (
            f"You are an expert {language} code reviewer. Provide detailed, actionable feedback on:\n"
            "1. Code quality and style\n"
            "2. Performance issues\n"
            "3. Security vulnerabilities\n"
            "4. Best practices\n"
            "5. Refactoring suggestions\n"
            "Be specific and provide code examples where helpful."
        )
        prompt = f"Review this {language} code and provide expert feedback:\n\n{code[:5000]}"
        return self.ask(prompt, system_prompt=system, model=CODING_MODEL, temperature=AI_TEMPERATURE_CODING)

    def generate_code(self, description: str, language: str = "python") -> str:
        """Generate production-ready code."""
        system = (
            f"You are an expert {language} developer. Generate clean, production-ready code that:\n"
            "1. Follows best practices\n"
            "2. Includes error handling\n"
            "3. Has clear documentation\n"
            "4. Is well-structured and maintainable\n"
            "Always include comments and docstrings."
        )
        prompt = f"Generate {language} code for:\n{description}"
        return self.ask(prompt, system_prompt=system, model=CODING_MODEL, temperature=AI_TEMPERATURE_CODING)

    def debug_error(self, error: str, context: str = "") -> str:
        """Advanced debugging assistance."""
        system = (
            "You are a debugging expert. Analyze errors deeply and provide:\n"
            "1. Root cause analysis\n"
            "2. Step-by-step solutions\n"
            "3. Prevention strategies\n"
            "4. Relevant code examples"
        )
        prompt = f"Error: {error}\n\nContext: {context}\n\nProvide detailed debugging help."
        return self.ask(prompt, system_prompt=system, model=ADVANCED_MODEL, temperature=AI_TEMPERATURE_CODING)

    def explain_code(self, code: str) -> str:
        """Deep code explanation."""
        system = (
            "You are a code explanation expert. Explain code clearly by:\n"
            "1. Breaking down the logic\n"
            "2. Explaining key concepts\n"
            "3. Highlighting important patterns\n"
            "4. Providing real-world context"
        )
        prompt = f"Explain this code in detail:\n\n{code[:5000]}"
        return self.ask(prompt, system_prompt=system, temperature=AI_TEMPERATURE_CHAT)

    def refactor_code(self, code: str, language: str = "python") -> str:
        """Professional code refactoring."""
        system = (
            f"You are a {language} refactoring expert. Improve code by:\n"
            "1. Enhancing readability\n"
            "2. Improving performance\n"
            "3. Reducing complexity\n"
            "4. Modernizing patterns\n"
            "Explain each change and why it's better."
        )
        prompt = f"Refactor this {language} code with improvements:\n\n{code[:5000]}"
        return self.ask(prompt, system_prompt=system, model=CODING_MODEL, temperature=AI_TEMPERATURE_CODING)

    def analyze_problem(self, problem: str) -> str:
        """Deep problem analysis."""
        system = (
            "You are an expert problem solver. Analyze problems by:\n"
            "1. Breaking down the issue\n"
            "2. Identifying root causes\n"
            "3. Proposing solutions\n"
            "4. Evaluating trade-offs"
        )
        prompt = f"Analyze this problem and provide solutions:\n\n{problem}"
        return self.ask(prompt, system_prompt=system, model=ADVANCED_MODEL, temperature=AI_TEMPERATURE_CREATIVE)

    def get_suggestions(self, topic: str, context: str = "") -> str:
        """Get creative suggestions."""
        system = (
            "You are a creative advisor. Provide thoughtful, actionable suggestions that are:\n"
            "1. Innovative\n"
            "2. Practical\n"
            "3. Well-reasoned\n"
            "4. Specific to the context"
        )
        prompt = f"Topic: {topic}\n\nContext: {context}\n\nProvide creative suggestions."
        return self.ask(prompt, system_prompt=system, model=ADVANCED_MODEL, temperature=AI_TEMPERATURE_CREATIVE)

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")


class AIClient:
    """Compatibility wrapper for AdvancedAIClient."""
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.client = AdvancedAIClient(api_key)
        self.model = model

    def ask(self, prompt: str, system_prompt: str = None) -> str:
        return self.client.ask(prompt, system_prompt=system_prompt, model=self.model)

    def code_review(self, code: str, language: str = "python") -> str:
        return self.client.code_review(code, language)

    def generate_code(self, description: str, language: str = "python") -> str:
        return self.client.generate_code(description, language)

    def debug_error(self, error: str, context: str = "") -> str:
        return self.client.debug_error(error, context)

    def explain_code(self, code: str) -> str:
        return self.client.explain_code(code)
