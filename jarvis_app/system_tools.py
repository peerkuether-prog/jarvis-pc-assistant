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
        "dd if=", "mkfs",
    ]
    for token in blocked:
        if token in lowered:
            return "This action is blocked for safety. I handle safe tasks and app control only."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return f"Command executed successfully.\n{result.stdout[:500]}" if result.stdout else "Command completed."
        else:
            return f"Command failed with error:\n{result.stderr[:500]}"
    except subprocess.TimeoutExpired:
        return "Command took too long to execute and was cancelled."
    except Exception as exc:
        return f"Could not execute command: {exc}"


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
        "vscode": "code.exe",
        "visual studio code": "code.exe",
        "python": "python.exe",
        "git": "git.exe",
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

    try:
        entries = sorted(child.name for child in target.iterdir())
        preview = "\n".join(entries[:50]) if entries else "Folder is empty."
        return f"Contents of {search_path}:\n{preview}"
    except PermissionError:
        return f"Permission denied accessing {search_path}"
    except Exception as exc:
        return f"Error listing folder: {exc}"


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

    preview = text[:5000] if text else "The file is empty."
    line_count = text.count("\n") + 1 if text else 0
    return f"File: {path} ({line_count} lines)\n---\n{preview}"


def write_file(path: str, content: str) -> str:
    try:
        target = Path(path).expanduser()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"File written successfully: {path}"
    except Exception as exc:
        return f"Could not write file: {exc}"


def delete_file(path: str) -> str:
    try:
        target = Path(path).expanduser()
        if not target.exists():
            return f"File does not exist: {path}"
        target.unlink()
        return f"File deleted: {path}"
    except Exception as exc:
        return f"Could not delete file: {exc}"


def get_system_summary() -> str:
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    user = os.getenv("USERNAME") or os.getenv("USER") or "User"
    processor = platform.processor() or "Unknown"
    return (
        f"System: {system} {release}\n"
        f"Version: {version}\n"
        f"Architecture: {machine}\n"
        f"Processor: {processor}\n"
        f"User: {user}"
    )


def search_web(query: str) -> str:
    if not query:
        return "No search query provided."
    url = "https://www.google.com/search?q=" + webbrowser.quote(query)
    webbrowser.open(url)
    return f"Searching Google for: {query}"


def get_file_info(path: str) -> str:
    try:
        target = Path(path).expanduser()
        if not target.exists():
            return f"Path does not exist: {path}"
        
        stat = target.stat()
        size_kb = stat.st_size / 1024
        is_dir = target.is_dir()
        type_str = "Folder" if is_dir else "File"
        
        return (
            f"{type_str}: {path}\n"
            f"Size: {size_kb:.2f} KB\n"
            f"Modified: {target.stat().st_mtime}\n"
            f"Is Directory: {is_dir}"
        )
    except Exception as exc:
        return f"Could not get file info: {exc}"
