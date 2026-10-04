import os
import platform
import subprocess
import webbrowser
from pathlib import Path


def safe_execute(command: str) -> str:
    if not command or not command.strip():
        return "No command provided."

    lowered = command.lower().strip()
    blocked = [
        "del ", "rm -rf", "format", "shutdown", "restart", "reboot",
        "taskkill", "rmdir /s", "powershell -command remove-item",
    ]
    for token in blocked:
        if token in lowered:
            return "This action is blocked for your safety. I can launch apps, open files, and do safe local actions only."

    try:
        subprocess.Popen(command, shell=True)
        return f"Command started: {command}"
    except Exception as exc:
        return f"Could not start command: {exc}"


def open_app(app_name: str) -> str:
    if not app_name:
        return "Please tell me which app or file to open."

    target = app_name.strip()
    app_map = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "terminal": "wt.exe",
        "explorer": "explorer.exe",
        "chrome": "msedge.exe",
        "edge": "msedge.exe",
        "browser": "msedge.exe",
        "file explorer": "explorer.exe",
    }
    normalized = target.lower()
    launch_target = app_map.get(normalized, target)

    if platform.system().lower() == "windows":
        try:
            os.startfile(launch_target)
            return f"Opened: {launch_target}"
        except Exception:
            pass

    try:
        subprocess.Popen(launch_target)
        return f"Opened: {launch_target}"
    except Exception as exc:
        return f"I could not open '{app_name}': {exc}"


def open_url(url: str) -> str:
    cleaned = url.strip()
    if not cleaned:
        return "No URL provided."
    if not cleaned.startswith(("http://", "https://")):
        cleaned = "https://" + cleaned
    webbrowser.open(cleaned)
    return f"Opening website: {cleaned}"


def list_dir(path: str) -> str:
    search_path = path.strip() or str(Path.home())
    target = Path(search_path).expanduser()
    if not target.exists():
        return f"Path does not exist: {search_path}"
    if not target.is_dir():
        return f"This is not a folder: {search_path}"

    entries = sorted(child.name for child in target.iterdir())
    preview = "\n".join(entries[:30]) if entries else "Folder is empty."
    return preview


def read_file(path: str) -> str:
    target = Path(path).expanduser()
    if not target.exists():
        return f"File not found: {path}"
    if target.is_dir():
        return "This is a folder, not a file."

    try:
        text = target.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return "I could not read this file. It may not be a valid text file."

    return text[:3000] if text else "The file is empty."


def get_system_summary() -> str:
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    user = os.getenv("USERNAME") or os.getenv("USER") or "User"
    return (
        f"System: {system} {release}\n"
        f"Version: {version}\n"
        f"Architecture: {machine}\n"
        f"User: {user}"
    )


def search_web(query: str) -> str:
    if not query:
        return "No search query provided."
    url = "https://www.google.com/search?q=" + webbrowser.quote(query)
    webbrowser.open(url)
    return f"Searching the web for: {query}"
