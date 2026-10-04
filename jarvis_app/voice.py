#!/usr/bin/env python3
"""Enhanced voice controller with better error handling and fallbacks."""

import logging
from datetime import datetime

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

logger = logging.getLogger(__name__)


class VoiceController:
    """Voice input/output with robust error handling and fallbacks."""

    def __init__(self):
        self.recognizer = None
        self.microphone = None
        self.engine = None
        self.voice_enabled = False
        self._initialize()

    def _initialize(self):
        """Initialize voice components with detailed logging."""
        if SR_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                self.voice_enabled = True
                logger.info("✓ Speech recognition initialized successfully")
            except Exception as e:
                logger.warning(f"✗ Speech recognition init failed: {e}")
                self.recognizer = None
                self.microphone = None
        else:
            logger.warning("✗ SpeechRecognition library not installed")

        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 165)
                self.engine.setProperty("volume", 0.95)
                logger.info("✓ Text-to-speech initialized successfully")
            except Exception as e:
                logger.warning(f"✗ Text-to-speech init failed: {e}")
                self.engine = None
        else:
            logger.warning("✗ pyttsx3 library not installed")

    def is_voice_available(self) -> bool:
        """Check if voice input is working."""
        return self.voice_enabled and self.recognizer is not None and self.microphone is not None

    def listen_once(self, timeout: int = 8, language: str = "en-US") -> str:
        """Listen for voice input with multiple fallbacks."""
        if not self.is_voice_available():
            logger.debug("Voice input not available")
            return ""

        try:
            with self.microphone as source:
                logger.info("Listening for audio...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=timeout
                )

            try:
                logger.debug("Recognizing audio (Google)...")
                text = self.recognizer.recognize_google(audio, language=language)
                logger.info(f"Recognized: {text}")
                return text.strip()
            except sr.UnknownValueError:
                logger.debug("Could not understand audio")
                return ""
            except sr.RequestError as e:
                logger.warning(f"Google API error: {e}")
                return ""
        except sr.WaitTimeoutError:
            logger.debug("Listening timeout")
            return ""
        except PermissionError:
            logger.error("Microphone permission denied")
            return ""
        except Exception as e:
            logger.error(f"Voice input error: {e}")
            return ""

    def speak(self, text: str, blocking: bool = True) -> bool:
        """Speak text with error handling."""
        if not text or not self.engine:
            return False

        try:
            logger.debug(f"Speaking: {text[:50]}...")
            self.engine.say(text)
            if blocking:
                self.engine.runAndWait()
            else:
                self.engine.startLoop(false)
            return True
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return False

    def stop_speaking(self):
        """Stop any ongoing speech."""
        if self.engine:
            try:
                self.engine.endLoop()
            except Exception:
                pass


def get_current_time() -> str:
    """Get current time in readable format."""
    return datetime.now().strftime("%I:%M %p")


def get_current_date() -> str:
    """Get current date in readable format."""
    return datetime.now().strftime("%A, %B %d, %Y")


def get_current_datetime() -> str:
    """Get current datetime in ISO format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_system_uptime() -> str:
    """Get system uptime (Linux/Mac only)."""
    try:
        with open("/proc/uptime", "r", encoding="utf-8") as fh:
            total_seconds = int(float(fh.read().split()[0]))
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours}h {minutes}m"
    except Exception:
        return "Uptime unavailable on this platform."
