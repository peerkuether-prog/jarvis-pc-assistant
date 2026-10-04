#!/usr/bin/env python3
"""PyInstaller build script for Jarvis Premium Windows EXE."""

import os
import sys
from pathlib import Path

# PyInstaller spec file generation
BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "dist"
BUILD_DIR = BASE_DIR / "build"

SPEC_CONTENT = '''# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('jarvis_app', 'jarvis_app')],
    hiddenimports=['PySide6', 'requests', 'speech_recognition', 'pyttsx3'],
    hookspath=[],
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Jarvis',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''

if __name__ == "__main__":
    spec_file = BASE_DIR / "jarvis.spec"
    spec_file.write_text(SPEC_CONTENT)
    print(f"✓ Generated {spec_file}")
    print("\nTo build the EXE, run:")
    print("  pyinstaller jarvis.spec --onefile --windowed")
