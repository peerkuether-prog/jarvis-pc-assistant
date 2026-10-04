from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from jarvis_app.assistant import JarvisAssistant
from jarvis_app.config import APP_TITLE, APP_VERSION, PROJECT_NAME


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Jarvis Settings")
        self.resize(420, 260)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"{PROJECT_NAME} {APP_VERSION}"))
        layout.addWidget(QLabel("AI: uses OpenAI-compatible chat completions if configured."))
        layout.addWidget(QLabel("Voice: optional. It will fall back gracefully if unavailable."))
        layout.addWidget(QLabel("Safety: destructive commands are blocked automatically."))

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)


class CodingPanel(QWidget):
    def __init__(self, assistant: JarvisAssistant):
        super().__init__()
        self.assistant = assistant
        self.setStyleSheet("background: #101820; color: white;")

        layout = QVBoxLayout(self)

        title = QLabel("Coding AI")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(title)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Paste code here or describe what you want generated...")
        self.input_box.setStyleSheet("background: #0d1721; border: 1px solid #2c3e50; border-radius: 8px; padding: 12px;")
        layout.addWidget(self.input_box, 3)

        actions = QHBoxLayout()
        for text, callback in [
            ("Review", self.review_code),
            ("Generate", self.generate_code),
            ("Explain", self.explain_code),
            ("Refactor", self.refactor_code),
        ]:
            button = QPushButton(text)
            button.clicked.connect(callback)
            actions.addWidget(button)
        layout.addLayout(actions)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background: #0d1721; border: 1px solid #2c3e50; border-radius: 8px; padding: 12px;")
        self.output.setPlaceholderText("AI coding output will appear here...")
        layout.addWidget(self.output, 2)

    def _code(self) -> str:
        return self.input_box.toPlainText().strip()

    def review_code(self):
        code = self._code()
        if not code:
            self.output.setPlainText("Paste code first.")
            return
        self.output.setPlainText("Reviewing code...")
        QApplication.processEvents()
        self.output.setPlainText(self.assistant.ai.code_review(code))

    def generate_code(self):
        prompt = self._code()
        if not prompt:
            self.output.setPlainText("Describe the code you want generated.")
            return
        self.output.setPlainText("Generating code...")
        QApplication.processEvents()
        self.output.setPlainText(self.assistant.ai.generate_code(prompt))

    def explain_code(self):
        code = self._code()
        if not code:
            self.output.setPlainText("Paste code first.")
            return
        self.output.setPlainText("Explaining code...")
        QApplication.processEvents()
        self.output.setPlainText(self.assistant.ai.explain_code(code))

    def refactor_code(self):
        code = self._code()
        if not code:
            self.output.setPlainText("Paste code first.")
            return
        self.output.setPlainText("Refactoring code...")
        QApplication.processEvents()
        self.output.setPlainText(self.assistant.ai.refactor_code(code))


class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.assistant = JarvisAssistant()
        self.setWindowTitle(f"{APP_TITLE} {APP_VERSION}")
        self.resize(1100, 720)

        self.central = QWidget()
        self.layout = QVBoxLayout(self.central)
        self.setCentralWidget(self.central)

        header = QHBoxLayout()
        title = QLabel(PROJECT_NAME)
        title.setStyleSheet("font-size: 30px; font-weight: 700; color: #7dd3fc;")
        header.addWidget(title)

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        header.addStretch()
        header.addWidget(settings_button)
        self.layout.addLayout(header)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { padding: 10px 18px; }")

        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)

        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_output.setPlaceholderText("Conversation will appear here...")
        self.chat_output.setStyleSheet("background: #0d1721; border: 1px solid #2c3e50; border-radius: 8px; padding: 12px;")
        chat_layout.addWidget(self.chat_output, 3)

        controls = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask Jarvis to open apps, check the time, search the web, read files, or code...")
        self.input_box.returnPressed.connect(self.send_message)
        controls.addWidget(self.input_box, 1)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        controls.addWidget(send_button)

        voice_button = QPushButton("Voice")
        voice_button.clicked.connect(self.handle_voice_input)
        controls.addWidget(voice_button)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_chat)
        controls.addWidget(clear_button)

        chat_layout.addLayout(controls)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #7dd3fc; font-size: 12px;")
        chat_layout.addWidget(self.status_label)

        self.tabs.addTab(chat_widget, "Chat")
        self.tabs.addTab(CodingPanel(self.assistant), "Coding AI")
        self.layout.addWidget(self.tabs, 1)

        self.append_message("System", "Jarvis is online. Ask me to open apps, check the system, browse files, or help with code.")

    def append_message(self, sender: str, text: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_output.append(f"[{timestamp}] {sender}: {text}")

    def clear_chat(self):
        self.chat_output.clear()
        self.append_message("System", "Conversation cleared.")

    def send_message(self):
        user_text = self.input_box.text().strip()
        if not user_text:
            return

        self.input_box.clear()
        self.append_message("You", user_text)
        self.status_label.setText("Thinking...")
        QApplication.processEvents()

        try:
            response = self.assistant.handle(user_text)
        except Exception as exc:
            response = f"I hit an error while handling that request: {exc}"

        self.append_message("Jarvis", response)
        self.status_label.setText("Ready")

        try:
            self.assistant.voice.speak(response)
        except Exception:
            pass

    def handle_voice_input(self):
        text = self.assistant.voice.listen_once(timeout=8)
        if not text:
            QMessageBox.information(self, "Voice input", "I couldn't understand that. Please type your request instead.")
            return
        self.input_box.setText(text)
        self.send_message()

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()


def launch_app():
    app = QApplication.instance() or QApplication([])
    window = JarvisWindow()
    window.show()
    app.exec()
