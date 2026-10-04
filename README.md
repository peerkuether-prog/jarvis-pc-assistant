# Jarvis Premium - Advanced PC Assistant

A premium desktop AI assistant for Windows with integrated coding AI, voice control, file management, and powerful automation.

## Features

### Core Assistant
- **Voice Chat**: Speak to Jarvis with natural language processing
- **App Launcher**: Open any Windows application by name
- **Web Integration**: Open websites and search the web instantly
- **File Management**: Read, write, delete, and browse files and folders
- **System Information**: Get detailed PC specs and uptime
- **Safe Command Execution**: Run safe commands with protection against dangerous actions

### Coding AI (Premium)
- **Code Review**: Get expert feedback on your code
- **Code Generation**: Generate code from descriptions
- **Debugging**: Get help understanding and fixing errors
- **Code Explanation**: Understand complex code
- **Code Refactoring**: Improve code quality and performance
- **Multi-language Support**: Python, JavaScript, Java, C++, C#, and more

### UI/UX
- Modern dark theme optimized for long coding sessions
- Tabbed interface: Chat + Code AI panels
- Real-time status updates
- Conversation history
- Settings panel

## Installation

1. Clone or download this repository
2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```
5. Run the app:
   ```bash
   python main.py
   ```

## Usage

### Chat Tab
- Type or use voice to interact with Jarvis
- Ask to open apps, search the web, read files, check system info, or get AI assistance
- Examples:
  - "Open notepad"
  - "Search web for Python tutorials"
  - "Read file C:/Users/me/notes.txt"
  - "What is the current time?"
  - "Tell me about my system"

### Code AI Tab
- Paste code and ask Jarvis to review, explain, refactor, or generate code
- Perfect for:
  - Code reviews before committing
  - Understanding unfamiliar code
  - Improving code quality
  - Generating boilerplate
  - Debugging errors

## Commands

### App & System
- `open [app name]` - Launch an application
- `search [query]` - Search Google
- `go to [url]` - Open a website
- `list folder [path]` - Show folder contents
- `read file [path]` - Read a text file
- `write file [path] with content: [text]` - Create/overwrite a file
- `delete file [path]` - Delete a file
- `file info [path]` - Get file details
- `system` - Show PC information

### Coding
- `review code [code]` - Get code review
- `generate code [description]` - Generate code from description
- `explain code [code]` - Explain what code does
- `refactor code [code]` - Improve code quality
- `debug [error]` - Help debug errors

## Requirements

- Windows 10 or later
- Python 3.10+
- Microphone for voice input (optional)
- OpenAI API key for AI features (optional, but recommended)

## Configuration

Edit `jarvis_app/config.py` to customize:
- AI model (default: gpt-4o-mini for chat, gpt-4o for coding)
- Theme colors
- App title and version

## Security

- Jarvis blocks dangerous commands (delete, shutdown, format, etc.)
- All API calls use HTTPS
- API key is kept in `.env` and never committed to version control
- File operations are confined to specified paths

## Roadmap

- System tray integration
- Custom hotkeys
- Plugin system for extensions
- Integration with calendar and email
- Advanced automation workflows
- Multi-voice support
- Dark/light theme switcher

## License

MIT

## Support

For issues, feature requests, or questions, please open an issue on GitHub.
