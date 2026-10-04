#!/usr/bin/env python3
"""Startup and registry management for Windows integration."""

import logging
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def get_executable_path() -> str:
    """Get the path to the executable (main.py or main.exe)."""
    if hasattr(sys, 'frozen'):
        return sys.executable
    return str(Path(__file__).parent.parent / "main.py")


def enable_startup(app_name: str = "Jarvis") -> bool:
    """Add Jarvis to Windows startup (Windows only)."""
    if sys.platform != "win32":
        logger.warning("Startup registration only works on Windows")
        return False

    try:
        import winreg
        exec_path = get_executable_path()
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{exec_path}"')
        logger.info(f"✓ {app_name} added to startup")
        return True
    except Exception as e:
        logger.error(f"Failed to enable startup: {e}")
        return False


def disable_startup(app_name: str = "Jarvis") -> bool:
    """Remove Jarvis from Windows startup (Windows only)."""
    if sys.platform != "win32":
        logger.warning("Startup management only works on Windows")
        return False

    try:
        import winreg
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, app_name)
        logger.info(f"✓ {app_name} removed from startup")
        return True
    except FileNotFoundError:
        logger.debug(f"{app_name} not in startup")
        return True
    except Exception as e:
        logger.error(f"Failed to disable startup: {e}")
        return False


def is_in_startup(app_name: str = "Jarvis") -> bool:
    """Check if Jarvis is in Windows startup (Windows only)."""
    if sys.platform != "win32":
        return False

    try:
        import winreg
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_READ) as key:
            try:
                winreg.QueryValueEx(key, app_name)
                return True
            except FileNotFoundError:
                return False
    except Exception as e:
        logger.error(f"Failed to check startup: {e}")
        return False
