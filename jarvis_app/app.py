from datetime import datetime

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from jarvis_app.assistant import JarvisAssistant
from jarvis_app.config import APP_TITLE, PROJECT_NAME


class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.assistant = JarvisAssistant()
        self.setWindowTitle(APP_TITLE)
        self.resize(1000, 700)

        central = QWidget()
        layout = QVBoxLayout(central)

        title = QPushButton(PROJECT_NAME)
        title.setEnabled(False)
        title.setStyleSheet(
            "QPushButton { background: #111827; border: 1px solid #374151; color: #E5E7EB; font-size: 24px; font-weight: 700; border-radius: 10px; padding: 12px; }"
        )
        layout.addWidget(title)

        self.chat_output = QPlainTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_output.setPlaceholderText("Assistant conversation will appear here...")
        self.chat_output.setStyleSheet(
            "QPlainTextEdit { background: #0f172a; color: #e5e7eb; border: 1px solid #334155; border-radius: 10px; padding: 12px; font-size: 14px; }"
        )
        layout.addWidget(self.chat_output, 1)

        controls = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask Jarvis to open apps, search the web, read files, or inspect the system...")
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

        layout.addLayout(controls)

        self.status_label = QPushButton("Ready")
        self.status_label.setEnabled(False)
        self.status_label.setStyleSheet(
            "QPushButton { background: #0b1220; border: 1px solid #1d4ed8; color: #93c5fd; border-radius: 8px; padding: 8px; }"
        )
        layout.addWidget(self.status_label)

        self.setCentralWidget(central)
        self.append_message("System", "Jarvis is online. Ask me to open apps, check your system, or browse the web.")

    def append_message(self, sender: str, text: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_output.appendPlainText(f"[{timestamp}] {sender}: {text}")

    def clear_chat(self):
        self.chat_output.clear()
        self.append_message("System", "Conversation cleared. How can I help?")

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
            response = f"I hit an error while processing the request: {exc}"

        self.append_message("Jarvis", response)
        self.status_label.setText("Ready")

        try:
            self.assistant.voice.speak(response)
        except Exception:
            pass

    def handle_voice_input(self):
        text = self.assistant.voice.listen_once()
        if not text:
            QMessageBox.information(self, "Voice input", "I could not understand what you said. Please type your request.")
            return
        self.input_box.setText(text)
        self.send_message()


def launch_app():
    app = QApplication.instance() or QApplication([])
    window = JarvisWindow()
    window.show()
    app.exec()
