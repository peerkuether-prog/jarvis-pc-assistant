import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

APP_TITLE = "Jarvis Premium"
PROJECT_NAME = "Jarvis"
APP_VERSION = "2.0"
DEFAULT_MODEL = "gpt-4o-mini"
CODING_MODEL = "gpt-4o"
OPENAI_BASE_URL = "https://api.openai.com/v1"

THEME_BG_PRIMARY = "#0f1419"
THEME_BG_SECONDARY = "#1a1f2e"
THEME_ACCENT = "#3b82f6"
THEME_TEXT_PRIMARY = "#e5e7eb"
THEME_TEXT_SECONDARY = "#9ca3af"
THEME_SUCCESS = "#10b981"
THEME_WARNING = "#f59e0b"
THEME_ERROR = "#ef4444"

def get_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "")

def get_home_dir() -> str:
    return str(Path.home())

def get_config_dir() -> Path:
    config_dir = Path.home() / ".jarvis"
    config_dir.mkdir(exist_ok=True)
    return config_dir
