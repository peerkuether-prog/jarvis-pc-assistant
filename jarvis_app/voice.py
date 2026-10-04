import os
from datetime import datetime

import pyttsx3
import speech_recognition as sr


class VoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = None
        self._setup_engine()

    def _setup_engine(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 170)
            self.engine.setProperty("volume", 1.0)
        except Exception:
            self.engine = None

    def listen_once(self, timeout: int = 8) -> str:
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
            return self.recognizer.recognize_google(audio).strip()
        except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
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
