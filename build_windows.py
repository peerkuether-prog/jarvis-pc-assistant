#!/usr/bin/env python
"""Build script for packaging Jarvis Premium as a Windows executable."""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
END = "\033[0m"


def print_header(text):
    print(f"\n{BLUE}{'='*60}{END}")
    print(f"{BLUE}{text}{END}")
    print(f"{BLUE}{'='*60}{END}")


def print_success(text):
    print(f"{GREEN}✓ {text}{END}")


def print_error(text):
    print(f"{RED}✗ {text}{END}")


def print_warning(text):
    print(f"{YELLOW}⚠ {text}{END}")


def run_command(cmd, description):
    """Run a shell command and report results."""
    print(f"\n{YELLOW}Running: {description}{END}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print_success(description)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed")
        print(f"Error: {e.stderr}")
        return False


def build_windows_package():
    """Build Jarvis Premium Windows package."""
    print_header("JARVIS PREMIUM - WINDOWS PACKAGE BUILDER")
    
    project_dir = Path(__file__).parent
    dist_dir = project_dir / "dist"
    build_dir = project_dir / "build"
    
    # Step 1: Check requirements
    print("\n[1/7] Checking requirements...")
    try:
        import PyInstaller
        print_success("PyInstaller installed")
    except ImportError:
        print_error("PyInstaller not installed")
        print("Install with: pip install pyinstaller")
        return False
    
    # Step 2: Clean previous builds
    print("\n[2/7] Cleaning previous builds...")
    for folder in [dist_dir, build_dir]:
        if folder.exists():
            shutil.rmtree(folder)
            print_success(f"Removed {folder.name}")
    
    # Step 3: Create icon placeholder (if needed)
    print("\n[3/7] Preparing resources...")
    icon_path = project_dir / "jarvis_app" / "icon.ico"
    if not icon_path.exists():
        print_warning("Icon file not found, using default")
    else:
        print_success("Icon file found")
    
    # Step 4: Build with PyInstaller
    print("\n[4/7] Building executable with PyInstaller...")
    pyinstaller_cmd = (
        f"pyinstaller --onefile --windowed --name=Jarvis "
        f"--distpath={dist_dir} --buildpath={build_dir} "
        f"--specpath={project_dir} "
        f"--add-data=jarvis_app:jarvis_app "
        f"--add-data=.env:. "
        f"--hidden-import=PySide6 "
        f"--hidden-import=speech_recognition "
        f"--hidden-import=pyttsx3 "
        f"--hidden-import=requests "
        f"--hidden-import=dotenv "
        f"main.py"
    )
    
    if not run_command(pyinstaller_cmd, "Building executable"):
        return False
    
    # Step 5: Verify build
    print("\n[5/7] Verifying build...")
    exe_path = dist_dir / "Jarvis.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print_success(f"Executable created: {exe_path} ({size_mb:.1f} MB)")
    else:
        print_error("Executable not found")
        return False
    
    # Step 6: Create launcher batch script
    print("\n[6/7] Creating launcher script...")
    batch_content = f"""@echo off
echo Starting Jarvis Premium...
cd /d "%~dp0"
start Jarvis.exe
exit
"""
    launcher_path = dist_dir / "run_jarvis.bat"
    launcher_path.write_text(batch_content)
    print_success(f"Launcher created: {launcher_path}")
    
    # Step 7: Create README for distribution
    print("\n[7/7] Creating distribution package...")
    readme_path = dist_dir / "README_DISTRIBUTION.txt"
    readme_content = f"""JARVIS PREMIUM - WINDOWS DISTRIBUTION
{'='*50}

Version: 3.0
Status: Ready to use

QUICK START:
1. Run 'run_jarvis.bat' or double-click 'Jarvis.exe'
2. First time? Create .env file with:
   OPENAI_API_KEY=your_key_here
3. Restart Jarvis

REQUIREMENTS:
- Windows 10 or later
- OpenAI API key (for AI features)
- Internet connection
- Microphone (for voice, optional)

FILES:
- Jarvis.exe - Main application
- run_jarvis.bat - Launcher script
- README_DISTRIBUTION.txt - This file

TROUBLESHOOTING:
- If app crashes, check .env file
- Verify API key is correct
- Ensure all dependencies installed
- Check Windows Defender isn't blocking

DOCUMENTATION:
See README_FINISHED.md in project for full docs

SUPPORT:
Open GitHub issues for bugs/features
"""
    readme_path.write_text(readme_content)
    print_success(f"README created: {readme_path}")
    
    # Final summary
    print_header("BUILD COMPLETE ✓")
    print(f"\n{GREEN}Jarvis Premium executable is ready!{END}")
    print(f"\nLocation: {dist_dir}")
    print(f"\nFiles:")
    for file in sorted(dist_dir.glob("*")):
        if file.is_file():
            size = file.stat().st_size
            if size > 1024*1024:
                size_str = f"{size/(1024*1024):.1f} MB"
            else:
                size_str = f"{size/1024:.1f} KB"
            print(f"  - {file.name} ({size_str})")
    
    print(f"\n{YELLOW}Next steps:{END}")
    print(f"1. Copy the 'dist' folder to your Windows PC")
    print(f"2. Run 'Jarvis.exe' or 'run_jarvis.bat'")
    print(f"3. Create .env file with API key if needed")
    print(f"4. Restart and enjoy Jarvis Premium!")
    
    return True


if __name__ == "__main__":
    success = build_windows_package()
    sys.exit(0 if success else 1)
