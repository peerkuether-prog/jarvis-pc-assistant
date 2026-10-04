#!/usr/bin/env python3
"""Professional desktop UI with tray mode, settings, and better controls."""

from __future__ import annotations

import logging
from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QSystemTrayIcon,
    QMenu,
)

from jarvis_app.assistant import JarvisAssistant
from jarvis_app.config import APP_TITLE, APP_VERSION, PROJECT_NAME
from jarvis_app.settings import AppSettings
from jarvis_app.startup import enable_startup, disable_startup, is_in_startup

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    """Advanced settings dialog."""

    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Jarvis Settings")
        self.resize(500, 600)
        self.setModal(True)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("API & Authentication"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("sk-...")
        self.api_key_input.setText(self.settings.api_key)
        self.api_key_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("OpenAI API Key:"))
        layout.addWidget(self.api_key_input)

        layout.addSpacing(12)
        layout.addWidget(QLabel("Startup & Window"))

        self.startup_checkbox = QCheckBox("Start Jarvis on system boot")
        self.startup_checkbox.setChecked(self.settings.start_on_boot)
        layout.addWidget(self.startup_checkbox)

        self.minimize_checkbox = QCheckBox("Start minimized to tray")
        self.minimize_checkbox.setChecked(self.settings.start_minimized)
        layout.addWidget(self.minimize_checkbox)

        self.tray_checkbox = QCheckBox("Enable tray mode (close to tray instead of exit)")
        self.tray_checkbox.setChecked(self.settings.tray_mode_enabled)
        layout.addWidget(self.tray_checkbox)

        layout.addSpacing(12)
        layout.addWidget(QLabel("Voice Settings"))

        self.auto_listen_checkbox = QCheckBox("Auto-listen after speaking (experimental)")
        self.auto_listen_checkbox.setChecked(self.settings.auto_listen)
        layout.addWidget(self.auto_listen_checkbox)

        layout.addWidget(QLabel("Voice language:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["en-US", "en-GB", "es-ES", "fr-FR", "de-DE"])
        self.language_combo.setCurrentText(self.settings.voice_language)
        layout.addWidget(self.language_combo)

        layout.addWidget(QLabel("TTS speed (100-300):"))
        self.tts_rate = QSpinBox()
        self.tts_rate.setRange(100, 300)
        self.tts_rate.setValue(self.settings.tts_rate)
        layout.addWidget(self.tts_rate)

        layout.addWidget(QLabel("TTS volume (0.0-1.0):"))
        self.tts_volume = QSpinBox()
        self.tts_volume.setRange(0, 100)
        self.tts_volume.setValue(int(self.settings.tts_volume * 100))
        self.tts_volume.setSuffix("%")
        layout.addWidget(self.tts_volume)

        layout.addSpacing(12)
        layout.addWidget(QLabel("AI Settings"))

        layout.addWidget(QLabel("Conversation memory (turns):"))
        self.memory_spin = QSpinBox()
        self.memory_spin.setRange(1, 50)
        self.memory_spin.setValue(self.settings.conversation_memory)
        layout.addWidget(self.memory_spin)

        layout.addStretch()

        buttons = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

    def save_settings(self):
        self.settings.api_key = self.api_key_input.text()
        self.settings.start_on_boot = self.startup_checkbox.isChecked()
        self.settings.start_minimized = self.minimize_checkbox.isChecked()
        self.settings.tray_mode_enabled = self.tray_checkbox.isChecked()
        self.settings.auto_listen = self.auto_listen_checkbox.isChecked()
        self.settings.voice_language = self.language_combo.currentText()
        self.settings.tts_rate = self.tts_rate.value()
        self.settings.tts_volume = self.tts_volume.value() / 100.0
        self.settings.conversation_memory = self.memory_spin.value()
        self.settings.save()

        if self.settings.start_on_boot:
            enable_startup()
        else:
            disable_startup()

        self.accept()


class CodingPanel(QWidget):
    """Coding AI panel with code generation, review, and refactoring."""

    def __init__(self, assistant: JarvisAssistant):
        super().__init__()
        self.assistant = assistant

        layout = QVBoxLayout(self)

        title = QLabel("Coding AI")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(title)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Paste code or describe what you want to generate...")
        layout.addWidget(self.input_box, 2)

        actions = QHBoxLayout()
        for text, callback in [
            ("Review", self.review_code),
            ("Generate", self.generate_code),
            ("Explain", self.explain_code),
            ("Refactor", self.refactor_code),
            ("Debug", self.debug_code),
        ]:
            button = QPushButton(text)
            button.clicked.connect(callback)
            actions.addWidget(button)
        layout.addLayout(actions)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("AI output will appear here...")
        layout.addWidget(self.output, 2)

    def _get_code(self) -> str:
        return self.input_box.toPlainText().strip()

    def _show_output(self, text: str):
        self.output.setPlainText(text or "No response from AI. Check API key.")

    def review_code(self):
        code = self._get_code()
        if not code:
            self._show_output("Paste code first.")
            return
        self.output.setPlainText("Reviewing code...")
        QApplication.processEvents()
        self._show_output(self.assistant.ai.code_review(code))

    def generate_code(self):
        prompt = self._get_code()
        if not prompt:
            self._show_output("Describe the code you want generated.")
            return
        self.output.setPlainText("Generating code...")
        QApplication.processEvents()
        self._show_output(self.assistant.ai.generate_code(prompt))

    def explain_code(self):
        code = self._get_code()
        if not code:
            self._show_output("Paste code first.")
            return
        self.output.setPlainText("Explaining code...")
        QApplication.processEvents()
        self._show_output(self.assistant.ai.explain_code(code))

    def refactor_code(self):
        code = self._get_code()
        if not code:
            self._show_output("Paste code first.")
            return
        self.output.setPlainText("Refactoring code...")
        QApplication.processEvents()
        self._show_output(self.assistant.ai.refactor_code(code))

    def debug_code(self):
        error = self._get_code()
        if not error:
            self._show_output("Paste error message or code first.")
            return
        self.output.setPlainText("Debugging...")
        QApplication.processEvents()
        self._show_output(self.assistant.ai.debug_error(error))


class JarvisWindow(QMainWindow):
    """Main application window with tray integration."""

    def __init__(self, settings: AppSettings):
        super().__init__()
        self.settings = settings
        self.assistant = JarvisAssistant(api_key=settings.api_key)
        self.setWindowTitle(f"{APP_TITLE} v{APP_VERSION}")
        self.resize(settings.window_width, settings.window_height)
        self.move(settings.window_x, settings.window_y)

        self._setup_ui()
        self._setup_tray()

    def _setup_ui(self):
        """Setup main UI."""
        self.central = QWidget()
        self.layout = QVBoxLayout(self.central)
        self.setCentralWidget(self.central)

        header = QHBoxLayout()
        title = QLabel(PROJECT_NAME)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #7dd3fc;")
        header.addWidget(title)

        settings_button = QPushButton("⚙ Settings")
        settings_button.clicked.connect(self.open_settings)
        voice_status = QLabel("🎤" if self.assistant.voice.is_voice_available() else "🔇")
        voice_status.setToolTip("Voice is available" if self.assistant.voice.is_voice_available() else "Voice not available")
        header.addStretch()
        header.addWidget(voice_status)
        header.addWidget(settings_button)
        self.layout.addLayout(header)

        self.tabs = QTabWidget()
        chat_widget = self._create_chat_tab()
        coding_widget = CodingPanel(self.assistant)
        self.tabs.addTab(chat_widget, "Chat")
        self.tabs.addTab(coding_widget, "Coding AI")
        self.layout.addWidget(self.tabs, 1)

        self.append_message("System", "Jarvis is online. Ask me to open apps, check the system, or help with code.")

    def _create_chat_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        layout.addWidget(self.chat_output, 2)

        controls = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your request or use Voice button...")
        self.input_box.returnPressed.connect(self.send_message)
        controls.addWidget(self.input_box, 1)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        controls.addWidget(send_button)

        voice_button = QPushButton("🎤 Voice")
        voice_button.clicked.connect(self.handle_voice_input)
        controls.addWidget(voice_button)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_chat)
        controls.addWidget(clear_button)

        layout.addLayout(controls)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #7dd3fc; font-size: 11px;")
        layout.addWidget(self.status_label)

        return widget

    def _setup_tray(self):
        """Setup system tray integration."""
        self.tray_icon = QSystemTrayIcon(self)

        tray_menu = QMenu(self)
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.showNormal)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self._on_tray_icon_activated)

    def _on_tray_icon_activated(self, reason):
        from PySide6.QtWidgets import QSystemTrayIcon
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.activateWindow()

    def closeEvent(self, event):
        """Handle window close."""
        if self.settings.tray_mode_enabled and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.quit_app()

    def quit_app(self):
        """Exit application."""
        self.settings.window_width = self.width()
        self.settings.window_height = self.height()
        self.settings.window_x = self.x()
        self.settings.window_y = self.y()
        self.settings.save()
        QApplication.quit()

    def append_message(self, sender: str, text: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_output.append(f"[{timestamp}] {sender}: {text}")

    def clear_chat(self):
        self.chat_output.clear()
        self.assistant.ai.clear_history()
        self.append_message("System", "Conversation cleared and memory reset.")

    def send_message(self):
        user_text = self.input_box.text().strip()
        if not user_text:
            return

        self.input_box.clear()
        self.append_message("You", user_text)
        self.status_label.setText("Processing...")
        QApplication.processEvents()

        try:
            response = self.assistant.handle(user_text)
        except Exception as exc:
            response = f"Error: {exc}"

        self.append_message("Jarvis", response)
        self.status_label.setText("Ready")

        try:
            self.assistant.voice.speak(response)
            if self.settings.auto_listen:
                QTimer.singleShot(1000, self.handle_voice_input)
        except Exception as e:
            logger.debug(f"Voice error: {e}")

    def handle_voice_input(self):
        if not self.assistant.voice.is_voice_available():
            QMessageBox.warning(self, "Voice", "Voice input is not available. Check audio setup.")
            return
        text = self.assistant.voice.listen_once(language=self.settings.voice_language)
        if not text:
            self.status_label.setText("Voice input failed")
            return
        self.input_box.setText(text)
        self.send_message()

    def open_settings(self):
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec():
            self.assistant.ai.context_window = self.settings.conversation_memory
            self.assistant.ai.api_key = self.settings.api_key


def launch_app():
    """Launch the application."""
    settings = AppSettings.load()
    app = QApplication.instance() or QApplication([])
    window = JarvisWindow(settings)
    if not settings.start_minimized:
        window.show()
    else:
        window.showMinimized()
    app.exec()
