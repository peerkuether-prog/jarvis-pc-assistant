from pathlib import Path
import os

from dotenv import load_dotenv

PROJECT_NAME = "Jarvis Assistant"
APP_TITLE = "Jarvis PC Assistant"
DEFAULT_MODEL = "gpt-4o-mini"


load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "")


def get_default_dir() -> str:
    return os.path.expanduser("~")
