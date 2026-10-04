#!/usr/bin/env python
"""Verify all imports and module integrity."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

print("Testing imports and module integrity...\n")

try:
    print("[1/10] Importing config...")
    from jarvis_app.config import (
        APP_TITLE, PROJECT_NAME, APP_VERSION, DEFAULT_MODEL, CODING_MODEL,
        get_api_key, get_home_dir, get_config_dir
    )
    print("✓ Config imports successful")
    print(f"   APP_TITLE: {APP_TITLE}")
    print(f"   PROJECT_NAME: {PROJECT_NAME}")
    print(f"   APP_VERSION: {APP_VERSION}")
except Exception as e:
    print(f"✗ Config import failed: {e}")
    sys.exit(1)

try:
    print("\n[2/10] Importing system_tools...")
    from jarvis_app.system_tools import (
        safe_execute, open_app, open_url, list_dir, read_file, write_file,
        delete_file, get_system_summary, search_web, get_file_info
    )
    print("✓ System tools imports successful")
except Exception as e:
    print(f"✗ System tools import failed: {e}")
    sys.exit(1)

try:
    print("\n[3/10] Importing voice...")
    from jarvis_app.voice import (
        VoiceController, get_current_time, get_current_date, get_current_datetime, get_system_uptime
    )
    print("✓ Voice imports successful")
except Exception as e:
    print(f"✗ Voice import failed: {e}")
    sys.exit(1)

try:
    print("\n[4/10] Importing ai_client...")
    from jarvis_app.ai_client import AIClient
    print("✓ AI client imports successful")
except Exception as e:
    print(f"✗ AI client import failed: {e}")
    sys.exit(1)

try:
    print("\n[5/10] Importing assistant...")
    from jarvis_app.assistant import JarvisAssistant, CodingAI
    print("✓ Assistant imports successful")
except Exception as e:
    print(f"✗ Assistant import failed: {e}")
    sys.exit(1)

try:
    print("\n[6/10] Importing app UI...")
    from jarvis_app.app import JarvisWindow, launch_app
    print("✓ App UI imports successful")
except Exception as e:
    print(f"✗ App UI import failed: {e}")
    sys.exit(1)

try:
    print("\n[7/10] Testing config functions...")
    home = get_home_dir()
    config_dir = get_config_dir()
    assert home and len(home) > 0
    assert config_dir and config_dir.exists()
    print(f"✓ Config functions work")
    print(f"   Home: {home}")
    print(f"   Config dir: {config_dir}")
except Exception as e:
    print(f"✗ Config functions failed: {e}")
    sys.exit(1)

try:
    print("\n[8/10] Testing voice functions...")
    time_str = get_current_time()
    date_str = get_current_date()
    dt_str = get_current_datetime()
    assert time_str and ":" in time_str
    assert date_str and len(date_str) > 0
    assert dt_str and len(dt_str) > 0
    print(f"✓ Voice functions work")
    print(f"   Time: {time_str}")
    print(f"   Date: {date_str}")
    print(f"   DateTime: {dt_str}")
except Exception as e:
    print(f"✗ Voice functions failed: {e}")
    sys.exit(1)

try:
    print("\n[9/10] Testing system summary...")
    summary = get_system_summary()
    assert summary and "System:" in summary
    print(f"✓ System summary works")
    print(f"   {summary[:100]}...")
except Exception as e:
    print(f"✗ System summary failed: {e}")
    sys.exit(1)

try:
    print("\n[10/10] Testing assistant initialization...")
    assistant = JarvisAssistant()
    assert assistant is not None
    assert hasattr(assistant, 'handle')
    assert hasattr(assistant, 'coding')
    assert hasattr(assistant, 'voice')
    assert hasattr(assistant, 'ai')
    assert hasattr(assistant, 'history')
    
    # Test basic response
    response = assistant.handle("test")
    assert isinstance(response, str) and len(response) > 0
    print(f"✓ Assistant initialization works")
    print(f"   Response to 'test': {response[:50]}...")
except Exception as e:
    print(f"✗ Assistant initialization failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✓ All import and integrity tests passed!")
print("="*50)
print("\nJarvis Premium is ready to run.")
print("Start with: python main.py")
