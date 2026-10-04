# Jarvis Premium - Quick Start Guide

## Installation Issues & Solutions

### PyAudio Not Found Error

**This is normal on Windows and is NOT a blocker.**

Jarvis works perfectly without PyAudio. Voice input uses Windows native audio APIs.

#### If you get `ERROR: Could not find a version that satisfies the requirement pyaudio`:

**Option 1: Ignore it (Recommended for Windows)**
```bash
# Just skip PyAudio - voice will still work
pip install -r requirements.txt --ignore-installed
python main.py
```

**Option 2: Use pipwin (If you want PyAudio)**
```bash
pip install pipwin
pipwin install pyaudio
pip install -r requirements.txt
python main.py
```

**Option 3: Use pre-built wheel**
```bash
# Download PyAudio wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then install:
pip install PyAudio-0.2.13-cp311-cp311-win_amd64.whl
pip install -r requirements.txt
python main.py
```

---

## What Works WITHOUT PyAudio

✓ **All voice features** - Speech recognition and text-to-speech work on Windows without PyAudio
✓ Chat AI
✓ Code review and generation  
✓ File management
✓ App launching
✓ Web search
✓ System information
✓ Text-to-speech
✓ Voice input (via Windows APIs)

---

## Complete Setup (No PyAudio Issues)

### 1. Clone Repository
```bash
git clone https://github.com/peerkuether-prog/jarvis-pc-assistant
cd jarvis-pc-assistant
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies (Skip PyAudio errors)
```bash
pip install PySide6 requests python-dotenv pyttsx3 SpeechRecognition pyinstaller
```

### 4. Create .env File
```
OPENAI_API_KEY=your_key_here
```

### 5. Verify Setup
```bash
python setup_check.py
```

### 6. Run the App
```bash
python main.py
```

---

## Alternative: Run Without Installing Anything

If you're having installation issues:

1. Download Python 3.10+ from https://www.python.org/
2. Open Command Prompt in project folder
3. Run:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install PySide6 requests python-dotenv pyttsx3 SpeechRecognition
   python main.py
   ```

---

## Voice Input Troubleshooting

### Voice button doesn't work
1. Check microphone is enabled in Windows Settings > Sound
2. Test microphone in Settings > Sound > Input devices
3. Try again - speak clearly

### Still having issues?
- Voice is optional - text chat works perfectly without it
- Try installing PyAudio if you really need it
- Or just type instead of using voice

---

## Common Error Messages

### "ModuleNotFoundError: No module named 'PyAudio'"
→ **Normal on Windows.** Ignore it. Just run `python main.py`

### "ModuleNotFoundError: No module named 'speech_recognition'"
→ Run: `pip install SpeechRecognition`

### "ModuleNotFoundError: No module named 'pyttsx3'"
→ Run: `pip install pyttsx3`

### "ModuleNotFoundError: No module named 'PySide6'"
→ Run: `pip install PySide6`

### App won't start
→ Run: `python setup_check.py` to diagnose

---

## Fast Install (Just Copy-Paste)

```bash
git clone https://github.com/peerkuether-prog/jarvis-pc-assistant
cd jarvis-pc-assistant
python -m pip install PySide6 requests python-dotenv pyttsx3 SpeechRecognition
echo OPENAI_API_KEY=your_key_here > .env
python main.py
```

---

## Still Having Issues?

1. Run diagnostic: `python setup_check.py`
2. Check you have Python 3.10+: `python --version`
3. Try fresh venv: `python -m venv venv2` then `venv2\Scripts\activate`
4. Reinstall basics: `pip install --upgrade pip setuptools wheel`
5. Try again: `python main.py`

---

**Bottom Line:** PyAudio errors can be safely ignored on Windows. Jarvis works great without it!
