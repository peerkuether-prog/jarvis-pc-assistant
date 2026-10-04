#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Voice module with fallback for PyAudio issues.
Works on Windows without PyAudio (uses native audio).
"""

import os
import logging
from datetime import datetime

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logging.warning("pyttsx3 not available - text-to-speech disabled")

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    logging.warning("speech_recognition not available - voice input disabled")


class VoiceController:
    """Voice input/output with fallback support."""

    def __init__(self):
        self.recognizer = None
        self.microphone = None
        self.engine = None
        self._setup()

    def _setup(self):
        """Setup voice components with error handling."""
        # Setup speech recognition
        if SR_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                logging.info("Speech recognition initialized")
            except Exception as e:
                logging.warning(f"Could not initialize speech recognition: {e}")
                self.recognizer = None
                self.microphone = None
        
        # Setup text-to-speech
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 170)
                self.engine.setProperty("volume", 1.0)
                logging.info("Text-to-speech initialized")
            except Exception as e:
                logging.warning(f"Could not initialize TTS: {e}")
                self.engine = None

    def listen_once(self, timeout: int = 8) -> str:
        """Listen for voice input with fallback."""
        if not self.recognizer or not self.microphone:
            logging.debug("Speech recognition not available")
            return ""

        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
            return self.recognizer.recognize_google(audio).strip()
        except sr.WaitTimeoutError:
            logging.debug("Voice input timeout")
            return ""
        except sr.UnknownValueError:
            logging.debug("Could not understand audio")
            return ""
        except sr.RequestError as e:
            logging.warning(f"Google Speech API error: {e}")
            return ""
        except Exception as e:
            logging.warning(f"Voice input error: {e}")
            return ""

    def speak(self, text: str) -> bool:
        """Speak text with fallback."""
        if not text or not self.engine:
            return False
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logging.warning(f"Text-to-speech error: {e}")
            return False


def get_current_time() -> str:
    return datetime.now().strftime("%I:%M %p")


def get_current_date() -> str:
    return datetime.now().strftime("%A, %B %d, %Y")


def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_system_uptime() -> str:
    try:
        with open("/proc/uptime", "r", encoding="utf-8") as handle:
            seconds = int(float(handle.read().split()[0]))
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours} hours, {minutes} minutes"
    except Exception:
        return "Uptime unavailable on this platform."
