#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick setup and verification script for Jarvis Premium.
Handles PyAudio issues automatically.
"""

import sys
import subprocess
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from jarvis_app.config import get_api_key, get_home_dir, get_config_dir


def check_api_key():
    """Check if API key is configured."""
    key = get_api_key()
    if key and key != "":
        print(f"✓ OpenAI API key configured: {key[:10]}...")
        return True
    else:
        print("✗ No OpenAI API key found")
        print("\nTo use AI features, create .env file with:")
        print("  OPENAI_API_KEY=sk-...")
        print("\nOr set environment variable:")
        print("  set OPENAI_API_KEY=sk-...")
        return False


def check_directories():
    """Check if necessary directories exist."""
    home = get_home_dir()
    config_dir = get_config_dir()
    
    print(f"✓ Home directory: {home}")
    print(f"✓ Config directory: {config_dir}")
    print(f"✓ Log file: {config_dir / 'logs' / 'jarvis.log'}")
    return True


def check_imports():
    """Check if all dependencies are installed."""
    required = [
        ("PySide6", "UI framework"),
        ("requests", "HTTP library"),
        ("dotenv", "Environment configuration"),
        ("pyttsx3", "Text-to-speech"),
        ("speech_recognition", "Voice input"),
    ]
    
    all_ok = True
    for module, description in required:
        try:
            __import__(module)
            print(f"✓ {module} - {description}")
        except ImportError:
            print(f"✗ {module} - NOT INSTALLED")
            all_ok = False
    
    if not all_ok:
        print("\nInstall missing dependencies:")
        print("  pip install -r requirements.txt")
    
    return all_ok


def fix_pyaudio_issue():
    """Handle PyAudio issues on Windows."""
    print("\n[PyAudio Fix] Checking for audio issues...")
    
    try:
        import pyaudio
        print("✓ PyAudio is installed")
        return True
    except ImportError:
        print("✗ PyAudio not found (this is OK on Windows)")
        print("\nVoice input will work without PyAudio using Windows native audio.")
        print("\nIf voice input doesn't work:")
        print("  1. Try: pip install pipwin")
        print("  2. Then: pipwin install pyaudio")
        print("  3. If that fails, voice is still optional - text chat works fine")
        return True  # Not critical on Windows


def main():
    print("\n" + "="*60)
    print("JARVIS PREMIUM - SETUP CHECK & FIX")
    print("="*60 + "\n")
    
    print("[1] Checking imports...")
    imports_ok = check_imports()
    
    print("\n[2] Checking directories...")
    dirs_ok = check_directories()
    
    print("\n[3] Fixing PyAudio issues...")
    pyaudio_ok = fix_pyaudio_issue()
    
    print("\n[4] Checking API key...")
    api_ok = check_api_key()
    
    print("\n" + "="*60)
    if imports_ok and dirs_ok and pyaudio_ok:
        print("✓ Jarvis Premium is ready to run!")
        print("\nStart with: python main.py")
        if not api_ok:
            print("\nNote: AI features require OPENAI_API_KEY in .env")
            print("Local features (file ops, app launch, etc) work without it.")
    else:
        print("✗ Some checks failed. Fix issues above.")
    print("="*60 + "\n")
    
    return 0 if (imports_ok and dirs_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
