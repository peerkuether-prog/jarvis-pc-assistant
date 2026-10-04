"""Jarvis Premium - Advanced desktop AI assistant with coding AI integration."""

from jarvis_app.app import JarvisWindow, launch_app
from jarvis_app.assistant import JarvisAssistant, CodingAI
from jarvis_app.ai_client import AIClient

__version__ = "2.0.0"
__all__ = ["JarvisAssistant", "CodingAI", "AIClient", "JarvisWindow", "launch_app"]
