# Jarvis Premium - Finished Production Version

A premium desktop AI assistant for Windows with integrated coding AI, voice control, file management, and advanced automation.

## ✓ Status: Production Ready

This is the finished, tested version of Jarvis Premium. All core features have been implemented and tested.

## Features

### Core Assistant
- ✓ Voice input and output with natural language processing
- ✓ App launcher (open any Windows application)
- ✓ Web integration (open websites, search Google)
- ✓ File management (read, write, delete, browse, get info)
- ✓ System information (PC specs, uptime)
- ✓ Safe command execution with protection against dangerous actions
- ✓ Action logging and history

### Coding AI (Integrated)
- ✓ Code review with expert feedback
- ✓ Code generation from descriptions
- ✓ Debugging assistance
- ✓ Code explanation
- ✓ Code refactoring
- ✓ Multi-language support (Python, JavaScript, Java, C++, C#, etc.)

### Premium UI
- ✓ Modern dark theme optimized for coding
- ✓ Multi-tab interface (Chat + Code AI)
- ✓ Real-time status updates
- ✓ Settings panel
- ✓ Professional design

## Installation

### Requirements
- Windows 10 or later
- Python 3.10+
- Microphone for voice (optional)
- OpenAI API key for AI features

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/peerkuether-prog/jarvis-pc-assistant
   cd jarvis-pc-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the app**
   ```bash
   python main.py
   ```

## Testing

### Run all tests
```bash
cd tests
python run_all_tests.py
```

### Run individual tests
```bash
# Import and integrity check
python tests/test_imports.py

# Command parsing
python tests/test_commands.py

# UI initialization
python tests/test_ui.py

# Full integration test
python tests/test_integration.py
```

## Usage

### Chat Tab
Type or speak to interact with Jarvis:

**App Control**
- "Open notepad"
- "Launch Visual Studio Code"
- "Open calculator"

**Web**
- "Search web for Python tutorials"
- "Go to github.com"
- "Open https://google.com"

**Files**
- "Read file C:/Users/me/notes.txt"
- "Write file C:/Users/me/test.txt with content: Hello"
- "Delete file C:/Users/me/old.txt"
- "List folder C:/Users/me/Documents"
- "File info C:/Users/me/document.pdf"

**System**
- "What time is it?"
- "What's today's date?"
- "Show system info"
- "Computer specs"

### Code AI Tab
Paste code and use the buttons:

**Review Code**
Paste your code → Click "Review Code" → Get expert feedback

**Generate Code**
Describe what you need → Click "Generate Code" → Get production-ready code

**Explain Code**
Paste code → Click "Explain Code" → Understand what it does

**Refactor Code**
Paste code → Click "Refactor Code" → Get improved version

## Commands Reference

| Command | Example | Use Case |
|---------|---------|----------|
| open [app] | "open notepad" | Launch applications |
| search [query] | "search web python" | Search Google |
| read file [path] | "read file ~/notes.txt" | Read text files |
| write file [path] with content | "write file ~/test.txt with content: hello" | Create/edit files |
| delete file [path] | "delete file ~/old.txt" | Delete files |
| list folder [path] | "list folder ~/Documents" | Browse folders |
| file info [path] | "file info ~/document.pdf" | Get file details |
| help | "help" | Show all capabilities |
| time | "what time" | Current time |
| date | "what's today" | Current date |
| system | "system info" | PC specifications |

## Security & Safety

✓ **Blocked Commands**: Dangerous operations (delete, shutdown, format) are blocked
✓ **HTTPS**: All API calls use secure connections
✓ **API Key**: Stored locally in `.env` and never committed
✓ **Sandboxed**: File operations confined to specified paths
✓ **Confirmation**: Risky actions require explicit permission

## Troubleshooting

### Voice input not working
- Check microphone is connected and enabled
- Test in system settings
- Ensure good ambient noise level

### AI features not working
- Verify OpenAI API key is correct in `.env`
- Check API key has valid credits
- Ensure internet connection is stable
- Check OpenAI API status

### App crashes
- Run in virtual environment
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version is 3.10+

## Configuration

Edit `jarvis_app/config.py` to customize:
- AI models used
- Theme colors
- App title and version

## Project Structure

```
jarvis-pc-assistant/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env.example           # Example env file
├── README.md              # This file
├── jarvis_app/
│   ├── __init__.py        # Package exports
│   ├── config.py          # Configuration
│   ├── ai_client.py       # OpenAI API client
│   ├── system_tools.py    # System operations
│   ├── voice.py           # Voice I/O
│   ├── assistant.py       # Core logic
│   └── app.py             # UI (PySide6)
└── tests/
    ├── run_all_tests.py   # Test runner
    ├── test_imports.py    # Import tests
    ├── test_commands.py   # Command parsing
    ├── test_ui.py         # UI tests
    ├── test_integration.py # Integration tests
    └── test_jarvis.py     # Unit tests
```

## Performance

- **Memory**: ~150 MB (depends on conversation history)
- **Startup**: ~2-3 seconds
- **Response Time**: 0.5-5 seconds (depending on AI model)
- **Voice**: 2-8 seconds for recognition and processing

## Requirements

- PySide6 (UI framework)
- requests (HTTP library)
- python-dotenv (configuration)
- pyttsx3 (text-to-speech)
- SpeechRecognition (voice input)
- pytest (testing)

## Future Enhancements

- System tray mode
- Hotkey activation
- Custom command presets
- Startup behavior
- Advanced automation workflows
- Calendar/email integration
- Multiple voice profiles
- Dark/light theme switcher
- Plugin system
- Conversation export

## License

MIT - Free for personal and commercial use

## Support

For issues or suggestions:
1. Check the troubleshooting section
2. Review test output for errors
3. Open an issue on GitHub
4. Include:
   - Python version
   - Windows version
   - Error message
   - Steps to reproduce

## Credits

Built with:
- OpenAI API for AI capabilities
- PySide6 for UI
- SpeechRecognition for voice input
- pyttsx3 for text-to-speech

---

**Version**: 2.0.0 (Production)
**Status**: ✓ Finished & Tested
**Last Updated**: 2026-10-04
