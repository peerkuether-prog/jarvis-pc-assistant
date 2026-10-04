# JARVIS PREMIUM - PRODUCTION DEPLOYMENT GUIDE

## Version 3.0 - Advanced AI Edition

### What's New in v3.0

✓ **Advanced AI Engine**
  - Conversation memory and context awareness
  - Multiple AI models for different tasks
  - Deep problem analysis and creative suggestions
  - Advanced debugging and code refactoring
  - Specialized prompts for each task type

✓ **Enhanced Performance**
  - Optimized API calls with timeout handling
  - Conversation history management
  - Improved error handling and logging
  - Better resource management

✓ **Windows Packaging**
  - PyInstaller build automation
  - Single-file executable
  - Launcher script included
  - Ready-to-distribute package

✓ **Production Quality**
  - Comprehensive logging
  - Better error messages
  - Improved configuration
  - Full documentation

## Building Windows Executable

### Option 1: Automated Build (Recommended)

```bash
# Install PyInstaller
pip install pyinstaller

# Run build script
python build_windows.py
```

This creates: `dist/Jarvis.exe`

### Option 2: Manual Build

```bash
pyinstaller --onefile --windowed --name=Jarvis main.py
```

### Distribution Package Contents

```
dist/
├── Jarvis.exe              # Main executable
├── run_jarvis.bat         # Windows launcher
└── README_DISTRIBUTION.txt # Quick start guide
```

## Deployment Instructions

### For Users

1. **Download**
   - Get `dist/` folder from GitHub releases
   - Or run `build_windows.py` yourself

2. **Setup**
   - Copy `dist/` to desired location
   - Create `.env` file in same folder:
     ```
     OPENAI_API_KEY=sk-...
     ```

3. **Run**
   - Double-click `run_jarvis.bat`
   - Or run `Jarvis.exe` directly

### For Developers

1. **Clone Repository**
   ```bash
   git clone https://github.com/peerkuether-prog/jarvis-pc-assistant
   cd jarvis-pc-assistant
   ```

2. **Setup Development Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run from Source**
   ```bash
   python main.py
   ```

4. **Build Executable**
   ```bash
   python build_windows.py
   ```

## System Requirements

**Minimum**
- Windows 10 or later
- 4 GB RAM
- 500 MB disk space
- .NET Framework 4.5+ (usually pre-installed)

**Recommended**
- Windows 11
- 8 GB RAM
- 1 GB disk space
- Fast internet connection

## API Configuration

### OpenAI API Key

1. Sign up at https://platform.openai.com
2. Create API key
3. Add to `.env` file:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### Models Used

- **gpt-4o-mini** - Default chat (fast, efficient)
- **gpt-4o** - Code review and generation (balanced)
- **gpt-4-turbo** - Advanced analysis (most capable)

### Cost Estimates

- ~1-3¢ per 100 chat messages
- ~2-5¢ per code review
- ~3-10¢ per complex analysis

## Troubleshooting Deployment

### Executable won't run

**Error: "Windows protected your PC"**
- Click "More info" → "Run anyway"
- Or disable SmartScreen temporarily

**Error: "API key not found"**
- Ensure `.env` is in same folder as `.exe`
- Format: `OPENAI_API_KEY=sk-...` (no spaces)

**Error: "Module not found"**
- Rebuild with: `python build_windows.py`
- Ensure all dependencies installed

### Performance Issues

- First startup: 5-10 seconds (normal)
- First API call: 3-5 seconds (normal)
- Check internet speed
- Check CPU/RAM usage in Task Manager

## GitHub Release Setup

### Creating a Release

1. **Build the package**
   ```bash
   python build_windows.py
   ```

2. **Create GitHub release**
   - Go to Releases page
   - Click "Create release"
   - Tag: `v3.0`
   - Title: "Jarvis Premium v3.0 - Advanced AI Edition"
   - Upload `dist/Jarvis.exe`
   - Upload `dist/run_jarvis.bat`
   - Upload `README_DISTRIBUTION.txt`

3. **Share Download Link**
   - Download link format:
     ```
     https://github.com/peerkuether-prog/jarvis-pc-assistant/releases/download/v3.0/Jarvis.exe
     ```

## Advanced Configuration

### Logging

Logs saved to: `C:\Users\{username}\.jarvis\logs\jarvis.log`

### Conversation History

Stored in memory during session. Clear with "Clear" button.

### Custom Models

Edit `config.py` to use different models:
```python
DEFAULT_MODEL = "gpt-4o-mini"      # Chat model
CODING_MODEL = "gpt-4o"             # Code model
ADVANCED_MODEL = "gpt-4-turbo"      # Complex tasks
```

## Performance Optimization

1. **Reduce API calls**
   - Use conversation history (enabled by default)
   - Batch related questions

2. **Improve response time**
   - Use faster models for simple tasks
   - Reduce max tokens if needed

3. **Save bandwidth**
   - Disable auto-history after 20 messages
   - Clear history for new sessions

## Security Best Practices

✓ Never share your API key
✓ Store `.env` in safe location
✓ Use environment variables for API key
✓ Don't commit `.env` to version control
✓ Use separate API keys for dev/prod
✓ Monitor API usage at OpenAI dashboard

## Support & Updates

- **Bug Reports**: GitHub Issues
- **Feature Requests**: GitHub Discussions
- **Updates**: Watch releases page
- **Documentation**: README_FINISHED.md

---

**Version**: 3.0 (Production)
**Status**: Ready for deployment
**Last Updated**: 2026-10-04
