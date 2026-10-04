import os
import time
from datetime import datetime

import pyttsx3
import speech_recognition as sr


class VoiceController:
    """Optional voice input/output abstraction for a desktop assistant."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = None
        self._set_up_engine()

    def _set_up_engine(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 170)
            self.engine.setProperty("volume", 1.0)
        except Exception:  # pragma: no cover - depends on system audio stack
            self.engine = None

    def listen_once(self) -> str:
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            text = self.recognizer.recognize_google(audio)
            return text.strip()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
        except Exception:
            return ""

    def speak(self, text: str) -> bool:
        if not text or not self.engine:
            return False
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception:
            return False


def get_current_time() -> str:
    return datetime.now().strftime("%I:%M %p")


def get_current_date() -> str:
    return datetime.now().strftime("%A, %B %d, %Y")


def get_system_uptime() -> str:
    try:
        with open("/proc/uptime", "r", encoding="utf-8") as handle:
            total_seconds = float(handle.read().split()[0])
        seconds = int(total_seconds)
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours} hours, {minutes} minutes"
    except Exception:
        return "Uptime unavailable on this platform."
