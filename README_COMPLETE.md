# Jarvis Premium v3.0 - Professional Desktop Assistant

A powerful AI-driven desktop assistant with chat, coding AI, file management, and system integration.

## Features

### 🤖 Smart AI
- Advanced conversation with memory and context
- Multi-model support (GPT-4, GPT-4 Turbo for coding)
- Specialized prompts for different tasks
- Code review, generation, refactoring, and debugging

### 🗣️ Voice
- Voice input with multiple language support
- Natural text-to-speech output
- Auto-listen mode (optional)
- Graceful fallback if audio unavailable

### 💻 System Integration
- Open apps and websites
- Browse folders and read/write files
- Web search capability
- System information and monitoring
- Safe command execution with safeguards

### 🎨 Professional UI
- Modern dark theme
- Chat interface with timestamps
- Dedicated coding AI panel
- Advanced settings dialog
- System tray integration
- Start on Windows boot

### 🔧 Production Features
- Persistent settings storage
- Conversation memory and history
- Error handling and logging
- Windows startup integration
- Tray mode with minimize to tray
- Packaged as Windows EXE

## Installation

### From Source

```bash
git clone https://github.com/peerkuether-prog/jarvis-pc-assistant
cd jarvis-pc-assistant
pip install -r requirements.txt
python main.py
```

### Windows EXE

Download the latest `Jarvis.exe` from releases and run it.

## Configuration

### API Key

1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Open Jarvis → Settings
3. Paste your API key and save

### Settings

- **Startup**: Start Jarvis on Windows boot
- **Voice**: Configure language, speed, volume
- **Tray**: Minimize to tray instead of exit
- **Memory**: Adjust conversation context window

## Building the EXE

```bash
pip install pyinstaller
python build_exe.py
pyinstaller jarvis.spec --onefile --windowed
```

The EXE will be in `dist/Jarvis.exe`.

## Usage Examples

### Chat
- "Open Chrome"
- "What's the time?"
- "Search the web for Python tutorials"
- "Read file C:/Users/You/document.txt"

### Coding AI
- Review code → Paste code, click Review
- Generate code → Describe what you want, click Generate
- Explain code → Paste code, click Explain
- Debug → Paste error, click Debug

### Voice
- Click the "🎤 Voice" button
- Speak your request
- Jarvis will respond

## Requirements

- Python 3.10+
- OpenAI API key (for AI features)
- Windows 10+ (for EXE and startup integration)
- Microphone (optional, for voice)

## Dependencies

- PySide6: UI framework
- requests: HTTP library
- python-dotenv: Environment config
- pyttsx3: Text-to-speech
- SpeechRecognition: Voice input
- PyInstaller: Build EXE

## Troubleshooting

### Voice not working
- Check microphone in Windows Settings
- Ensure speaker/audio is working
- Try typing instead of voice

### AI responses empty
- Verify API key is correct
- Check internet connection
- Try a simpler question

### EXE won't start
- Ensure all dependencies installed
- Run `python main.py` to test
- Check `.jarvis/logs/jarvis.log` for errors

## License

MIT License - See LICENSE file

## Support

For issues, suggestions, or contributions, visit:
https://github.com/peerkuether-prog/jarvis-pc-assistant
