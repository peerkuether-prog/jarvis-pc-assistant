import os
import platform
import subprocess
import webbrowser
from pathlib import Path


def safe_execute(command: str) -> str:
    """Execute a safe, non-destructive command in a controlled way."""
    command = command.strip()
    if not command:
        return "No command provided."

    blocked = ["del ", "rm -rf", "format", "shutdown", "restart", "reboot", "taskkill"]
    lowered = command.lower()
    for keyword in blocked:
        if keyword in lowered:
            return "This action is blocked for safety. I can open apps, files, or folders, but I won't run destructive commands."

    try:
        subprocess.Popen(command, shell=True)
        return f"Command started: {command}"
    except Exception as exc:  # pragma: no cover - depends on OS
        return f"Could not start command: {exc}"


def open_app(app_name: str) -> str:
    """Open a common Windows application or file."""
    if not app_name:
        return "I need the name of the app or file to open."

    normalized = app_name.strip().lower()
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
    }

    target = app_map.get(normalized, app_name)

    if platform.system().lower() == "windows":
        try:
            os.startfile(target)
            return f"Opened: {target}"
        except Exception:
            pass

    try:
        subprocess.Popen(target)
        return f"Opened: {target}"
    except Exception as exc:
        return f"I could not open '{app_name}': {exc}"


def open_url(url: str) -> str:
    """Open a website in the default browser."""
    cleaned = url.strip()
    if not cleaned:
        return "No URL provided."
    if not cleaned.startswith(("http://", "https://")):
        cleaned = "https://" + cleaned
    webbrowser.open(cleaned)
    return f"Opening website: {cleaned}"


def list_dir(path: str) -> str:
    """List files in a directory."""
    search_path = path.strip() or str(Path.home())
    if not Path(search_path).exists():
        return f"Path does not exist: {search_path}"

    entries = []
    for child in sorted(Path(search_path).iterdir()):
        entries.append(child.name)
    return "\n".join(entries[:25]) if entries else "Folder is empty."


def read_file(path: str) -> str:
    """Read a text file and return its contents (up to a limit)."""
    target = Path(path).expanduser()
    if not target.exists():
        return f"File not found: {path}"
    if target.is_dir():
        return "This is a folder, not a file."

    try:
        text = target.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return "I could not read that file. It may not be a valid text file."

    preview = text[:2000]
    return preview if preview else "The file is empty."


def get_system_summary() -> str:
    """Return a brief summary of the current machine."""
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
