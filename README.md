# Jarvis PC Assistant

A polished desktop assistant for Windows PCs with a sleek interface, voice interaction, local command execution, and AI-assisted responses.

Features
- AI chat panel with a built-in assistant mode
- Optional voice input and speech output
- Quick system actions: date/time, system info, app launching, website opening, file browsing
- Safe command handling with confirmation for risky actions
- Web search and local folder/file tools
- Windows-first desktop UX designed to feel like a personal assistant

Project structure
- `main.py` — app entry point
- `jarvis_app/app.py` — main PySide6 UI and assistant logic
- `jarvis_app/ai_client.py` — AI client and smart fallback responses
- `jarvis_app/config.py` — configuration and environment support
- `jarvis_app/system_tools.py` — local file and system helpers
- `jarvis_app/voice.py` — speech recognition and text-to-speech

Quick start
1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python main.py
   ```
4. Optional: set `OPENAI_API_KEY` in a `.env` file for AI-powered responses.

Example `.env`
```env
OPENAI_API_KEY=your_key_here
```

Notes
- Voice input depends on microphone access and may require additional setup on some machines.
- This project is intentionally designed to be safe: destructive actions require confirmation.
- For best results on Windows, run from a Python environment with access to the system microphone and speakers.
