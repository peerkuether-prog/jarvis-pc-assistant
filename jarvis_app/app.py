from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from jarvis_app.assistant import JarvisAssistant
from jarvis_app.config import APP_TITLE, PROJECT_NAME, APP_VERSION, THEME_BG_PRIMARY, THEME_BG_SECONDARY, THEME_ACCENT


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Jarvis Settings")
        self.resize(400, 300)
        self.setModal(True)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Jarvis {APP_VERSION}"))
        layout.addWidget(QLabel("Settings page coming soon."))
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)


class CodingPanel(QWidget):
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Coding AI Assistant"))
        
        self.code_input = QPlainTextEdit()
        self.code_input.setPlaceholderText("Paste code here or ask me to generate, review, explain, or refactor code...")
        self.code_input.setStyleSheet(f"background: {THEME_BG_SECONDARY}; color: #e5e7eb; border-radius: 8px; padding: 8px;")
        layout.addWidget(self.code_input, 1)
        
        button_layout = QHBoxLayout()
        
        review_btn = QPushButton("Review Code")
        review_btn.clicked.connect(self.review_code)
        button_layout.addWidget(review_btn)
        
        generate_btn = QPushButton("Generate Code")
        generate_btn.clicked.connect(self.generate_code)
        button_layout.addWidget(generate_btn)
        
        explain_btn = QPushButton("Explain Code")
        explain_btn.clicked.connect(self.explain_code)
        button_layout.addWidget(explain_btn)
        
        refactor_btn = QPushButton("Refactor Code")
        refactor_btn.clicked.connect(self.refactor_code)
        button_layout.addWidget(refactor_btn)
        
        layout.addLayout(button_layout)
        
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet(f"background: {THEME_BG_SECONDARY}; color: #e5e7eb; border-radius: 8px; padding: 8px;")
        layout.addWidget(self.output, 1)
    
    def review_code(self):
        code = self.code_input.toPlainText()
        if not code:
            self.output.setPlainText("Please paste code first.")
            return
        self.output.setPlainText("Analyzing code...")
        QApplication.processEvents()
        result = self.assistant.coding.review_code(code)
        self.output.setPlainText(result)
    
    def generate_code(self):
        description = self.code_input.toPlainText()
        if not description:
            self.output.setPlainText("Please describe what code you need.")
            return
        self.output.setPlainText("Generating code...")
        QApplication.processEvents()
        result = self.assistant.coding.generate_code(description)
        self.output.setPlainText(result)
    
    def explain_code(self):
        code = self.code_input.toPlainText()
        if not code:
            self.output.setPlainText("Please paste code first.")
            return
        self.output.setPlainText("Analyzing code...")
        QApplication.processEvents()
        result = self.assistant.coding.explain(code)
        self.output.setPlainText(result)
    
    def refactor_code(self):
        code = self.code_input.toPlainText()
        if not code:
            self.output.setPlainText("Please paste code first.")
            return
        self.output.setPlainText("Refactoring code...")
        QApplication.processEvents()
        result = self.assistant.coding.refactor(code)
        self.output.setPlainText(result)


class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.assistant = JarvisAssistant()
        self.setWindowTitle(f"{APP_TITLE} v{APP_VERSION}")
        self.resize(1200, 800)
        
        # Main widget and layout
        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel(PROJECT_NAME)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {THEME_ACCENT};")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        settings_btn = QPushButton("⚙ Settings")
        settings_btn.clicked.connect(self.open_settings)
        settings_btn.setMaximumWidth(120)
        header_layout.addWidget(settings_btn)
        
        main_layout.addLayout(header_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget {{ background: {THEME_BG_PRIMARY}; }}
            QTabBar::tab {{ background: {THEME_BG_SECONDARY}; color: #e5e7eb; padding: 10px 20px; }}
            QTabBar::tab:selected {{ background: {THEME_ACCENT}; }}
        """)
        
        # Chat Tab
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        
        self.chat_output = QPlainTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_output.setPlaceholderText("Jarvis conversation will appear here...")
        self.chat_output.setStyleSheet(
            f"QPlainTextEdit {{ background: {THEME_BG_SECONDARY}; color: #e5e7eb; border: 1px solid #334155; border-radius: 10px; padding: 12px; font-size: 13px; }}"
        )
        chat_layout.addWidget(self.chat_output, 1)
        
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask Jarvis to open apps, read files, code, search, or anything else...")
        self.input_box.returnPressed.connect(self.send_message)
        self.input_box.setStyleSheet(
            f"QLineEdit {{ background: {THEME_BG_SECONDARY}; color: #e5e7eb; border: 1px solid #334155; border-radius: 8px; padding: 8px; }}"
        )
        input_layout.addWidget(self.input_box, 1)
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        send_button.setMaximumWidth(80)
        input_layout.addWidget(send_button)
        
        voice_button = QPushButton("🎤")
        voice_button.clicked.connect(self.handle_voice_input)
        voice_button.setMaximumWidth(50)
        input_layout.addWidget(voice_button)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_chat)
        clear_button.setMaximumWidth(80)
        input_layout.addWidget(clear_button)
        
        chat_layout.addLayout(input_layout)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {THEME_ACCENT}; font-size: 12px;")
        chat_layout.addWidget(self.status_label)
        
        self.tabs.addTab(chat_widget, "Chat")
        
        # Coding Tab
        coding_panel = CodingPanel(self.assistant)
        self.tabs.addTab(coding_panel, "Code AI")
        
        main_layout.addWidget(self.tabs, 1)
        
        self.setCentralWidget(central)
        
        # Style main window
        self.setStyleSheet(f"QMainWindow {{ background: {THEME_BG_PRIMARY}; }}")
        
        # Welcome message
        self.append_message("System", f"{PROJECT_NAME} Premium is online. Ask me to open apps, code, search, read files, or get system info.")

    def append_message(self, sender: str, text: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_output.appendPlainText(f"[{timestamp}] {sender}: {text}")

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
            self.assistant.log_action(user_text, response)
        except Exception as exc:
            response = f"I hit an error: {exc}"

        self.append_message("Jarvis", response)
        self.status_label.setText("Ready")

        try:
            self.assistant.voice.speak(response)
        except Exception:
            pass

    def handle_voice_input(self):
        self.status_label.setText("Listening...")
        QApplication.processEvents()
        text = self.assistant.voice.listen_once()
        if not text:
            self.status_label.setText("Ready")
            QMessageBox.information(self, "Voice input", "I could not understand. Please type your request.")
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
