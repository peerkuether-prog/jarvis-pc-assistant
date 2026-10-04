from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from jarvis_app.ai_client import AdvancedAIClient
from jarvis_app.config import APP_TITLE, PROJECT_NAME, get_home_dir
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
from jarvis_app.voice import VoiceController, get_current_date, get_current_time

logger = logging.getLogger(__name__)


@dataclass
class IntentResult:
    intent: str
    payload: Dict[str, Any] = field(default_factory=dict)
    response: Optional[str] = None


class IntentRouter:
    """A cleaner intent-based command system for Jarvis."""

    def __init__(self, assistant: "JarvisAssistant"):
        self.assistant = assistant

    def route(self, text: str) -> IntentResult:
        query = text.strip()
        if not query:
            return IntentResult("empty", response="I am ready. Ask me to open apps, check your system, or do something safe.")

        lowered = query.lower()

        if lowered in {"hello", "hi", "hey", "good morning", "good evening", "good afternoon"}:
            return IntentResult("greeting", response=f"Hello! I am {PROJECT_NAME}. How can I help you today?")

        if lowered in {"help", "what can you do", "capabilities"}:
            return IntentResult(
                "help",
                response=(
                    "I can open apps, browse folders, read files, search the web, check system info, "
                    "run safe commands, answer questions, and help with coding tasks."
                ),
            )

        if "time" in lowered and "date" not in lowered:
            return IntentResult("time", response=f"The current time is {get_current_time()}.")

        if "date" in lowered:
            return IntentResult("date", response=f"Today is {get_current_date()}.")

        if "system" in lowered or "computer" in lowered or "device" in lowered or "spec" in lowered:
            return IntentResult("system", response=get_system_summary())

        if "uptime" in lowered:
            return IntentResult("uptime", response=f"System uptime: {self.assistant.system_uptime()}")

        if re.search(r"\b(open|launch)\s+(https?://|www\.)", lowered):
            return IntentResult("open_url", response=open_url(query.split(None, 1)[1].strip()))

        if re.search(r"\b(open|launch)\b", lowered):
            target = re.sub(r"^(open|launch)\s+", "", query, flags=re.I).strip()
            if not target:
                return IntentResult("open_error", response="What would you like me to open?")
            return IntentResult("open_app", response=open_app(target))

        if re.search(r"\b(search|look up|find)\b", lowered):
            target = re.sub(r"^(search|look up|find)\s+(web\s+)?", "", query, flags=re.I).strip()
            if not target:
                return IntentResult("search_error", response="What do you want me to search for?")
            return IntentResult("search", response=search_web(target))

        if re.search(r"\b(go to|open website|open url)\b", lowered):
            target = re.sub(r"^(go to|open website|open url)\s+", "", query, flags=re.I).strip()
            if not target:
                return IntentResult("open_url_error", response="What website should I open?")
            return IntentResult("open_url", response=open_url(target))

        if "list folder" in lowered or "list files" in lowered or "show files" in lowered or "show folder" in lowered:
            folder = re.sub(r"^(list folder|list files|show files|show folder)\s+", "", query, flags=re.I).strip()
            return IntentResult("list_dir", response=list_dir(folder or get_home_dir()))

        if "read file" in lowered:
            path = re.sub(r"^read file\s+", "", query, flags=re.I).strip()
            return IntentResult("read_file", response=read_file(path))

        if "write file" in lowered or "create file" in lowered:
            try:
                if " with content" in lowered:
                    expr = re.sub(r"^(write file|create file)\s+", "", query, flags=re.I)
                    path_part, content_part = expr.split(" with content", 1)
                    return IntentResult("write_file", response=write_file(path_part.strip(), content_part.strip()))
                if " content:" in lowered:
                    expr = re.sub(r"^(write file|create file)\s+", "", query, flags=re.I)
                    path_part, content_part = expr.split(" content:", 1)
                    return IntentResult("write_file", response=write_file(path_part.strip(), content_part.strip()))
            except Exception:
                pass
            return IntentResult("write_file_error", response="Use: write file C:/path/file.txt with content: hello")

        if "delete file" in lowered:
            path = re.sub(r"^delete file\s+", "", query, flags=re.I).strip()
            return IntentResult("delete_file", response=delete_file(path))

        if "file info" in lowered or "info about" in lowered:
            path = re.sub(r"^(file info|info about)\s+", "", query, flags=re.I).strip()
            return IntentResult("file_info", response=get_file_info(path))

        if "run command" in lowered or "execute" in lowered:
            command = re.sub(r"^(run command|execute)\s+", "", query, flags=re.I).strip()
            if not command:
                return IntentResult("command_error", response="What command should I run?")
            return IntentResult("command", response=safe_execute(command))

        if re.search(r"\b(review code|code review|debug|explain code|refactor code|generate code|write code)\b", lowered):
            return IntentResult("coding", payload={"raw": query})

        if "shutdown" in lowered or "restart" in lowered or "format" in lowered or "delete all" in lowered:
            return IntentResult("blocked", response="I will not perform destructive or risky actions without explicit confirmation.")

        return IntentResult("fallback", response=self.assistant.ai_fallback(query))


class JarvisAssistant:
    """Clean core assistant logic."""

    def __init__(self, api_key: str = ""):
        self.ai = AdvancedAIClient(api_key=api_key)
        self.voice = VoiceController()
        self.router = IntentRouter(self)
        self.history: List[Dict[str, str]] = []

    def system_uptime(self) -> str:
        try:
            with open("/proc/uptime", "r", encoding="utf-8") as fh:
                total_seconds = float(fh.read().split()[0])
            hours, remainder = divmod(int(total_seconds), 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours} hours, {minutes} minutes"
        except Exception:
            return "Uptime unavailable on this platform."

    def ai_fallback(self, query: str) -> str:
        response = self.ai.ask(query, system_prompt="You are Jarvis, a helpful desktop assistant. Keep responses brief, clear, and practical.")
        if response:
            return response
        return "I can help with local tasks, web searches, files, system info, and coding help. Try asking me to open an app, check the time, or read a file."

    def handle(self, user_text: str) -> str:
        result = self.router.route(user_text)

        if result.intent == "coding":
            raw = result.payload.get("raw", "")
            lowered = raw.lower()
            if "review code" in lowered or "code review" in lowered:
                code = re.sub(r"^(review code|code review)\s+", "", raw, flags=re.I).strip()
                return self.ai.code_review(code or "")
            if "generate code" in lowered or "write code" in lowered:
                prompt = re.sub(r"^(generate code|write code)\s+", "", raw, flags=re.I).strip()
                return self.ai.generate_code(prompt or raw)
            if "explain code" in lowered:
                code = re.sub(r"^explain code\s+", "", raw, flags=re.I).strip()
                return self.ai.explain_code(code or raw)
            if "refactor code" in lowered:
                code = re.sub(r"^refactor code\s+", "", raw, flags=re.I).strip()
                return self.ai.refactor_code(code or raw)
            if "debug" in lowered:
                message = re.sub(r"^debug\s+", "", raw, flags=re.I).strip()
                return self.ai.debug_error(message or raw)
            return self.ai_fallback(raw)

        response = result.response or self.ai_fallback(user_text)
        self.history.append({"user": user_text, "assistant": response})
        return response

    def clear_history(self):
        self.history.clear()
