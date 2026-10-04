from datetime import datetime
from pathlib import Path

from jarvis_app.ai_client import AIClient
from jarvis_app.config import PROJECT_NAME, get_home_dir, get_config_dir
from jarvis_app.system_tools import (
    delete_file,
    get_file_info,
    get_system_summary,
    list_dir,
    open_app,
    open_url,
    read_file,
    safe_execute,
    search_web,
    write_file,
)
from jarvis_app.voice import VoiceController, get_current_date, get_current_datetime, get_current_time


class CodingAI:
    """Specialized AI for coding tasks."""

    def __init__(self, api_key: str = ""):
        self.ai = AIClient(api_key=api_key)

    def review_code(self, code: str, language: str = "python") -> str:
        return self.ai.code_review(code, language)

    def generate_code(self, description: str, language: str = "python") -> str:
        return self.ai.generate_code(description, language)

    def debug(self, error: str, context: str = "") -> str:
        return self.ai.debug_error(error, context)

    def explain(self, code: str) -> str:
        return self.ai.explain_code(code)

    def refactor(self, code: str, language: str = "python") -> str:
        system = f"You are a {language} refactoring expert. Provide improved, cleaner, more efficient code with explanations."
        prompt = f"Refactor this {language} code:\n\n{code}"
        return self.ai.ask(prompt, system_prompt=system)


class JarvisAssistant:
    def __init__(self, api_key: str = ""):
        self.ai = AIClient(api_key=api_key)
        self.coding = CodingAI(api_key=api_key)
        self.voice = VoiceController()
        self.history = []

    def log_action(self, user_input: str, response: str):
        """Log conversation to history."""
        timestamp = get_current_datetime()
        self.history.append({"timestamp": timestamp, "user": user_input, "jarvis": response})

    def handle(self, user_text: str) -> str:
        text = user_text.strip()
        if not text:
            return "I am ready. Ask me to open apps, search, code, read files, or check your system."

        lowered = text.lower()
        if lowered.startswith("jarvis"):
            text = text[6:].strip()
            lowered = text.lower()

        # Greetings
        if lowered in {"hello", "hi", "hey", "good morning", "good evening", "good afternoon"}:
            return f"Hello! I am {PROJECT_NAME}. How can I help today?"

        if lowered in {"help", "what can you do", "capabilities"}:
            return (
                "I can: open apps and websites, read and write files, list folders, run safe commands, search the web, "
                "check system info, review code, generate code, debug errors, explain code, refactor code, "
                "tell time and date, and answer questions with AI."
            )

        # Time and Date
        if "time" in lowered and "date" not in lowered:
            return f"The current time is {get_current_time()}."
        if "date" in lowered:
            return f"Today is {get_current_date()}."

        # System Info
        if "system" in lowered or "computer" in lowered or "device" in lowered:
            return get_system_summary()

        # App and URL Control
        if "open " in lowered:
            target = text.replace("open ", "", 1).strip()
            if target.lower().startswith("http"):
                return open_url(target)
            return open_app(target)

        if "launch " in lowered:
            target = text.replace("launch ", "", 1).strip()
            return open_app(target)

        # Web Search
        if "search web" in lowered or "search the web" in lowered:
            query = text.replace("search web", "", 1).replace("search the web", "", 1).strip()
            return search_web(query)
        if "search" in lowered:
            query = text.replace("search", "", 1).strip()
            if query:
                return search_web(query)

        if "open website" in lowered or "open url" in lowered or "go to" in lowered:
            query = text.replace("open website", "", 1).replace("open url", "", 1).replace("go to", "", 1).strip()
            return open_url(query)

        # File Operations
        if "list folder" in lowered or "show files" in lowered or "list files" in lowered:
            query = text.replace("list folder", "", 1).replace("show files", "", 1).replace("list files", "", 1).strip()
            return list_dir(query or get_home_dir())

        if "read file" in lowered:
            path = text.replace("read file", "", 1).strip()
            return read_file(path)

        if "write file" in lowered or "create file" in lowered:
            # Parse "write file /path/to/file with content: data"
            parts = text.replace("write file", "", 1).replace("create file", "", 1).strip()
            if " with " in parts or " content " in parts:
                try:
                    path, content = parts.split(" with ", 1) if " with " in parts else parts.split(" content ", 1)
                    return write_file(path.strip(), content.strip())
                except Exception:
                    return "Usage: write file /path with content: your text here"
            return "Usage: write file /path with content: your text here"

        if "delete file" in lowered:
            path = text.replace("delete file", "", 1).strip()
            return delete_file(path)

        if "file info" in lowered or "info about" in lowered:
            path = text.replace("file info", "", 1).replace("info about", "", 1).strip()
            return get_file_info(path)

        # Command Execution
        if "run command" in lowered or "execute" in lowered:
            command = text.replace("run command", "", 1).replace("execute", "", 1).strip()
            return safe_execute(command)

        # Coding AI Features
        if "review code" in lowered or "code review" in lowered:
            prompt = text.replace("review code", "", 1).replace("code review", "", 1).strip()
            return self.coding.review_code(prompt)

        if "generate code" in lowered or "write code" in lowered:
            prompt = text.replace("generate code", "", 1).replace("write code", "", 1).strip()
            return self.coding.generate_code(prompt)

        if "debug" in lowered or "what's wrong" in lowered:
            error_text = text.replace("debug", "", 1).replace("what's wrong", "", 1).strip()
            return self.coding.debug(error_text)

        if "explain code" in lowered:
            code = text.replace("explain code", "", 1).strip()
            return self.coding.explain(code)

        if "refactor code" in lowered:
            code = text.replace("refactor code", "", 1).strip()
            return self.coding.refactor(code)

        # Block dangerous actions
        if "shutdown" in lowered or "restart" in lowered or "delete" in lowered:
            return "I will not perform destructive actions without explicit confirmation. I can help with safe tasks instead."

        # AI Fallback
        ai_response = self.ai.ask(text)
        if ai_response:
            return ai_response

        return (
            "I can help with local computer tasks, app control, file management, web search, system info, and coding assistance. "
            "What would you like me to do?"
        )
