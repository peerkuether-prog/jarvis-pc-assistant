from datetime import datetime

from jarvis_app.ai_client import AIClient
from jarvis_app.config import APP_TITLE, PROJECT_NAME, get_home_dir
from jarvis_app.system_tools import (
    get_system_summary,
    get_system_uptime,
    list_dir,
    open_app,
    open_url,
    read_file,
    safe_execute,
    search_web,
)
from jarvis_app.voice import VoiceController, get_current_date, get_current_time


class JarvisAssistant:
    def __init__(self, api_key: str = ""):
        self.ai = AIClient(api_key=api_key)
        self.voice = VoiceController()

    def handle(self, user_text: str) -> str:
        text = user_text.strip()
        if not text:
            return "I am ready. Try asking me to open an app, search the web, read a file, or check your system."

        lowered = text.lower()
        if lowered.startswith("jarvis"):
            text = text[6:].strip()
            lowered = text.lower()

        if lowered in {"hello", "hi", "hey", "good morning", "good evening"}:
            return f"Hello! I am {PROJECT_NAME}. How can I help today?"

        if lowered in {"help", "what can you do"}:
            return (
                "I can open apps, open websites, read files, list folders, check the time and date, show system info, "
                "search the web, and answer questions with AI if you add an API key."
            )

        if "time" in lowered and "date" not in lowered:
            return f"The current time is {get_current_time()}."

        if "date" in lowered:
            return f"Today is {get_current_date()}."

        if "uptime" in lowered:
            return f"System uptime: {get_system_uptime()}"

        if "system" in lowered or "computer" in lowered or "device" in lowered:
            return get_system_summary()

        if "open " in lowered:
            target = text.replace("open ", "", 1).strip()
            if target.lower().startswith("http"):
                return open_url(target)
            return open_app(target)

        if "launch " in lowered:
            target = text.replace("launch ", "", 1).strip()
            return open_app(target)

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

        if "list folder" in lowered or "show files" in lowered or "list files" in lowered:
            query = text.replace("list folder", "", 1).replace("show files", "", 1).replace("list files", "", 1).strip()
            return list_dir(query or get_home_dir())

        if "read file" in lowered:
            path = text.replace("read file", "", 1).strip()
            return read_file(path)

        if "run command" in lowered:
            command = text.replace("run command", "", 1).strip()
            return safe_execute(command)

        if "shutdown" in lowered or "restart" in lowered or "delete" in lowered:
            return "I will not perform destructive actions without confirmation. I can handle safe tasks and app control instead."

        ai_response = self.ai.ask(text)
        if ai_response:
            return ai_response

        return (
            "I can help with local computer tasks, website opening, file browsing, system checks, and safe automation. "
            "Try asking me to open an app or read a file."
        )
