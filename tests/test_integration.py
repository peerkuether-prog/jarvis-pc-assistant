#!/usr/bin/env python
"""Integration tests for Jarvis Premium."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis_app.assistant import JarvisAssistant
from jarvis_app.config import get_home_dir, get_api_key


def test_full_workflow():
    """Test a complete workflow of the assistant."""
    print("\n=== Jarvis Premium Integration Test ===")
    
    assistant = JarvisAssistant()
    
    # Test 1: Greeting
    print("\n[Test 1] Greeting")
    response = assistant.handle("hello")
    print(f"Response: {response}")
    assert response and len(response) > 0
    print("✓ Greeting works")
    
    # Test 2: Help
    print("\n[Test 2] Help command")
    response = assistant.handle("help")
    print(f"Response: {response}")
    assert response and "can" in response.lower()
    print("✓ Help works")
    
    # Test 3: Time
    print("\n[Test 3] Current time")
    response = assistant.handle("what's the time")
    print(f"Response: {response}")
    assert ":" in response or "time" in response.lower()
    print("✓ Time retrieval works")
    
    # Test 4: Date
    print("\n[Test 4] Current date")
    response = assistant.handle("what's today")
    print(f"Response: {response}")
    assert response and len(response) > 0
    print("✓ Date retrieval works")
    
    # Test 5: System info
    print("\n[Test 5] System information")
    response = assistant.handle("system")
    print(f"Response: {response}")
    assert "System" in response
    print("✓ System info works")
    
    # Test 6: List folder
    print("\n[Test 6] List home folder")
    response = assistant.handle(f"list folder {get_home_dir()}")
    print(f"Response (truncated): {response[:200]}...")
    assert response and len(response) > 0
    print("✓ Folder listing works")
    
    # Test 7: File operations
    print("\n[Test 7] Write and read file")
    test_file = Path(get_home_dir()) / "jarvis_test.txt"
    write_response = assistant.handle(f"write file {test_file} with content: Jarvis Test Content")
    print(f"Write response: {write_response}")
    assert "written" in write_response.lower()
    
    read_response = assistant.handle(f"read file {test_file}")
    print(f"Read response (truncated): {read_response[:200]}...")
    assert "Jarvis Test Content" in read_response or "test" in read_response.lower()
    
    delete_response = assistant.handle(f"delete file {test_file}")
    print(f"Delete response: {delete_response}")
    assert "deleted" in delete_response.lower()
    print("✓ File operations work")
    
    # Test 8: Safety check
    print("\n[Test 8] Safety blocking")
    response = assistant.handle("shutdown")
    print(f"Response: {response}")
    assert "destructive" in response.lower() or "cannot" in response.lower()
    print("✓ Safety blocking works")
    
    # Test 9: Logging
    print("\n[Test 9] Action logging")
    initial_history = len(assistant.history)
    assistant.handle("test log entry")
    assert len(assistant.history) == initial_history + 1
    print("✓ Action logging works")
    
    # Test 10: Voice controller init
    print("\n[Test 10] Voice controller")
    assert assistant.voice is not None
    assert hasattr(assistant.voice, 'listen_once')
    assert hasattr(assistant.voice, 'speak')
    print("✓ Voice controller initialized")
    
    print("\n=== All Integration Tests Passed ✓ ===")


if __name__ == "__main__":
    test_full_workflow()
