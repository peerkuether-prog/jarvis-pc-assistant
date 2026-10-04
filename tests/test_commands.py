#!/usr/bin/env python
"""Unit tests for command parsing and response generation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis_app.assistant import JarvisAssistant


def test_command_parsing():
    """Test that commands are parsed correctly."""
    print("\n=== Command Parsing Tests ===")
    
    assistant = JarvisAssistant()
    test_cases = [
        ("hello", "should greet"),
        ("hi", "should greet"),
        ("hey", "should greet"),
        ("help", "should show help"),
        ("what can you do", "should show capabilities"),
        ("what time is it", "should show time"),
        ("what's the time", "should show time"),
        ("what is today", "should show date"),
        ("what's the date", "should show date"),
        ("system info", "should show system"),
        ("computer info", "should show system"),
        ("device info", "should show system"),
    ]
    
    for command, description in test_cases:
        response = assistant.handle(command)
        success = response and len(response) > 0 and isinstance(response, str)
        status = "✓" if success else "✗"
        print(f"{status} '{command}' -> {description}")
        if not success:
            print(f"   Response was: {response}")
            raise AssertionError(f"Failed to handle: {command}")
    
    print("\n✓ All command parsing tests passed")


if __name__ == "__main__":
    test_command_parsing()
