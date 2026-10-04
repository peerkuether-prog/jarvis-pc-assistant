# Installation and First Run Guide

## Quick Start (5 minutes)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
Create `.env` file with:
```env
OPENAI_API_KEY=sk-...
```

### 3. Run Tests (Optional but Recommended)
```bash
cd tests
python run_all_tests.py
```

### 4. Launch the App
```bash
python main.py
```

## What to Expect

### First Launch
- Window opens with Jarvis branding
- Chat tab shows "Jarvis Premium is online"
- Voice button (🎤) is ready
- Settings button (⚙) visible

### Chat Tab
1. Try: "Hello"
   - Should respond with greeting
2. Try: "What time is it?"
   - Should show current time
3. Try: "Help"
   - Should list all capabilities
4. Try: "Open notepad"
   - Should launch notepad
5. Try: "Search web for Python"
   - Should open Google with search

### Code AI Tab
1. Paste Python code
2. Click "Review Code"
3. Get professional code review with suggestions

### Voice Input
1. Click 🎤 button
2. Speak clearly (e.g., "What time is it?")
3. Jarvis recognizes and responds

## Troubleshooting First Run

### "Module not found" error
```bash
# Install missing dependencies
pip install -r requirements.txt
```

### "API Key not found" error
- Create `.env` file in project root
- Add: `OPENAI_API_KEY=your_key_here`
- Restart app

### Voice not working
- Windows: Ensure microphone is enabled in Settings > Sound
- Test microphone in Settings
- Speak clearly into microphone
- Check sound levels are adequate

### App crashes on startup
- Verify Python 3.10+: `python --version`
- Reinstall PySide6: `pip install --upgrade PySide6`
- Run in fresh virtual environment

## Next Steps

1. **Customize Settings**
   - Click ⚙ Settings button
   - Configure preferences

2. **Use Code AI Features**
   - Go to "Code AI" tab
   - Paste code snippets
   - Use review/generate/refactor buttons

3. **Explore Commands**
   - Type "help" to see all commands
   - Try different app names
   - Test file operations

4. **Voice Control**
   - Practice voice commands
   - Works best in quiet environments
   - Natural language is supported

## Performance Notes

- **First response**: May take 3-5 seconds (API initialization)
- **Subsequent responses**: 1-3 seconds
- **Voice recognition**: 2-8 seconds depending on audio length
- **File operations**: Instant for local files

## Daily Usage Tips

1. Keep the window minimized and use voice
2. Use "Search web" for quick information
3. Save frequently used commands
4. Voice works best in quiet environments
5. Use Code AI tab for programming help

## Getting Help

- Run: `python tests/run_all_tests.py` to verify installation
- Check README_FINISHED.md for full documentation
- Review test output for any issues
- Ensure all imports work: `python tests/test_imports.py`

---

Jarvis Premium is ready to use! Enjoy your new AI assistant.
