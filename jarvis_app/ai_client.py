import webbrowser
from datetime import datetime
from typing import List

from jarvis_app.ai_client import AIClient
from jarvis_app.config import APP_TITLE, PROJECT_NAME, get_default_dir
from jarvis_app.system_tools import (
    get_system_summary,
    list_dir,
    open_app,
    open_url,
    read_file,
    safe_execute,
    search_web,
)
from jarvis_app.voice import VoiceController, get_current_date, get_current_time


class JarvisAssistant:
    """Core orchestration layer for assistant behavior."""

    def __init__(self, api_key: str = ""):
        self.ai = AIClient(api_key=api_key)
        self.voice = VoiceController()

    def build_local_response(self, user_text: str) -> str:
        text = user_text.strip()
        lowered = text.lower()

        if lowered.startswith("jarvis"):
            text = text[6:].strip()
            lowered = text.lower()

        if not text:
            return "I am ready. Ask me to open an app, search the web, check the time, or tell me about the system."

        if lowered in {"hello", "hi", "hey", "good morning", "good evening"}:
            return f"Hello! I am {PROJECT_NAME}. How can I help you today?"

        if "time" in lowered and "date" not in lowered:
            return f"The current time is {get_current_time()}."

        if "date" in lowered:
            return f"Today is {get_current_date()}."

        if "system" in lowered or "computer" in lowered or "device" in lowered:
            return get_system_summary()

        if "open " in lowered:
            target = text.split("open ", 1)[1].strip()
            return open_app(target)

        if "search" in lowered and "web" in lowered:
            query = text.replace("search web", "", 1).replace("search", "", 1).strip()
            return search_web(query)

        if "search" in lowered:
            query = text.replace("search", "", 1).strip()
            return search_web(query)

        if "website" in lowered or "url" in lowered or "open https" in lowered:
            url = text.replace("open ", "", 1).replace("website", "", 1).replace("url", "", 1).strip()
            return open_url(url)

        if "list files" in lowered or "show files" in lowered or "list folder" in lowered:
            folder = text.replace("list files", "").replace("show files", "").replace("list folder", "").strip()
            return list_dir(folder or get_default_dir())

        if "read file" in lowered:
            file_path = text.replace("read file", "", 1).strip()
            return read_file(file_path)

        if "run" in lowered and "command" in lowered:
            command = text.replace("run command", "", 1).replace("run", "", 1).strip()
            return safe_execute(command)

        if "weather" in lowered:
            return "Weather is not yet connected in this local build. I can open a weather website or check other local system information instead."

        if "shutdown" in lowered or "restart" in lowered or "delete" in lowered:
            return "I cannot perform destructive commands without confirmation. I can help with safe tasks only."

        response = self.ai.ask(text)
        if response:
            return response

        return (
            f"I can help with local tasks on this computer. Try asking me to open an app, check the time, read a file, "
            f"search the web, or tell you about the system."
        )


class JarvisWindow:
    """Main UI window for the Jarvis PC assistant."""

    def __init__(self):
        self.app = None
        self.assistant = JarvisAssistant()
        self.window = None
        self.chat_area = None
        self.input_box = None
        self.status_label = None
        self.voice_enabled = True

    def build(self):
        from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget

        self.app = QApplication.instance() or QApplication([])
        self.window = QMainWindow()
        self.window.setWindowTitle(APP_TITLE)
        self.window.resize(980, 660)

        central_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel(PROJECT_NAME)
        title.setStyleSheet("font-size: 24px; font-weight: 700; margin-bottom: 10px;")
        layout.addWidget(title)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setPlaceholderText("Assistant conversation will appear here...")
        self.chat_area.setStyleSheet("background: #101820; color: #F2F2F2; border: 1px solid #2B3A55; border-radius: 8px; padding: 12px; font-size: 14px;")
        layout.addWidget(self.chat_area, 1)

        controls = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask Jarvis to open apps, search the web, check the time, or analyze your PC...")
        self.input_box.returnPressed.connect(self.send_message)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)

        voice_button = QPushButton("Voice")
        voice_button.clicked.connect(self.handle_voice_input)

        controls.addWidget(self.input_box, 1)
        controls.addWidget(send_button)
        controls.addWidget(voice_button)
        layout.addLayout(controls)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #7DD3FC; font-size: 12px;")
        layout.addWidget(self.status_label)

        central_widget.setLayout(layout)
        self.window.setCentralWidget(central_widget)

        self.append_message("System", "Jarvis is ready. Ask me to open an app, check the system, search the web, or read a file.")
        self.window.show()

    def append_message(self, sender: str, text: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_area.append(f"[{timestamp}] {sender}: {text}")

    def send_message(self):
        user_text = self.input_box.text().strip()
        if not user_text:
            return

        self.input_box.clear()
        self.append_message("You", user_text)
        self.status_label.setText("Thinking...")
        self.window.repaint()

        response = self.assistant.build_local_response(user_text)
        self.append_message("Jarvis", response)
        self.status_label.setText("Ready")

        if self.voice_enabled:
            self.assistant.voice.speak(response)

    def handle_voice_input(self):
        text = self.assistant.voice.listen_once()
        if text:
            self.input_box.setText(text)
            self.send_message()
        else:
            self.append_message("System", "Voice input was not recognized. Please type your request or try again.")


def launch_app():
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    window = JarvisWindow()
    window.build()
    app.exec()
