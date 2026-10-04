# Jarvis PC Assistant

A premium desktop assistant for Windows PCs with chat, voice, local system controls, and AI-powered assistance.

Features
- Voice chat and text chat
- App and site launcher
- File browser and file reader
- Safe local command execution
- System info and uptime reporting
- OpenAI-compatible AI fallback
- Modern dark UI

Run the app
1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python main.py
   ```
4. Optional: create a `.env` file with:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

Notes
- Voice features depend on a microphone and speakers being available.
- Unsafe actions are blocked by default.
- This is designed to be practical, safe, and extensible for Windows desktop use.
