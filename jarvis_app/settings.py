#!/usr/bin/env python3
"""Settings management for Jarvis."""

import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

from jarvis_app.config import get_config_dir

logger = logging.getLogger(__name__)


@dataclass
class AppSettings:
    """User-configurable application settings."""
    api_key: str = ""
    start_on_boot: bool = False
    start_minimized: bool = False
    tray_mode_enabled: bool = True
    auto_listen: bool = False
    voice_language: str = "en-US"
    tts_rate: int = 165
    tts_volume: float = 0.95
    conversation_memory: int = 10
    theme: str = "dark"
    window_width: int = 1100
    window_height: int = 720
    window_x: int = 100
    window_y: int = 100

    @classmethod
    def load(cls) -> "AppSettings":
        """Load settings from disk or return defaults."""
        settings_file = get_config_dir() / "settings.json"
        if settings_file.exists():
            try:
                with open(settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(**data)
            except Exception as e:
                logger.warning(f"Failed to load settings: {e}")
                return cls()
        return cls()

    def save(self):
        """Save settings to disk."""
        settings_file = get_config_dir() / "settings.json"
        try:
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(asdict(self), f, indent=2)
            logger.info(f"Settings saved to {settings_file}")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
