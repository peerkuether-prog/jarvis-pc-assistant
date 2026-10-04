import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

APP_TITLE = "Jarvis PC Assistant"
PROJECT_NAME = "Jarvis"
DEFAULT_MODEL = "gpt-4o-mini"
OPENAI_BASE_URL = "https://api.openai.com/v1"


def get_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "")


def get_home_dir() -> str:
    return str(Path.home())
