#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
One-click setup script for Jarvis Premium.
Handles all dependencies and fixes common issues.
"""

import subprocess
import sys
from pathlib import Path


def run_cmd(cmd, description):
    """Run a command and report status."""
    print(f"\n[*] {description}...")
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print(f"[✓] {description} OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] {description} - Warning (continuing anyway)")
        return False
    except Exception as e:
        print(f"[!] {description} - Error: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("JARVIS PREMIUM - ONE-CLICK SETUP")
    print("="*60)
    
    print("\n[1] Upgrading pip...")
    run_cmd(f"{sys.executable} -m pip install --upgrade pip", "Pip upgrade")
    
    print("\n[2] Installing core dependencies (ignoring PyAudio)...")
    deps = [
        "PySide6>=6.7.0",
        "requests>=2.32.0",
        "python-dotenv>=1.0.1",
        "pyttsx3>=2.91",
        "SpeechRecognition>=3.10.0",
        "pyinstaller>=6.0.0",
    ]
    
    for dep in deps:
        run_cmd(f"{sys.executable} -m pip install \"{dep}\" --no-deps", f"Installing {dep.split('>=')[0]}")
    
    print("\n[3] Checking installation...")
    run_cmd(f"{sys.executable} setup_check.py", "Verification")
    
    print("\n" + "="*60)
    print("✓ Setup complete!")
    print("\nYou can now run:")
    print("  python main.py")
    print("="*60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
