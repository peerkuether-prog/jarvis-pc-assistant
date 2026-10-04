#!/usr/bin/env python
"""End-to-end UI test mock (without displaying the window)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication
from jarvis_app.app import JarvisWindow


def test_ui_initialization():
    """Test that the UI initializes without errors."""
    print("\n=== UI Initialization Test ===")
    
    try:
        # Create QApplication if needed
        app = QApplication.instance() or QApplication([])
        
        print("[1/3] Creating main window...")
        window = JarvisWindow()
        assert window is not None
        print("✓ Main window created")
        
        print("[2/3] Checking UI components...")
        assert hasattr(window, 'chat_output')
        assert hasattr(window, 'input_box')
        assert hasattr(window, 'status_label')
        assert hasattr(window, 'assistant')
        assert hasattr(window, 'tabs')
        print("✓ All UI components present")
        
        print("[3/3] Testing UI methods...")
        # Test append_message
        window.append_message("Test", "This is a test message")
        text = window.chat_output.toPlainText()
        assert "Test" in text and "This is a test message" in text
        print("✓ Message appending works")
        
        print("\n✓ UI initialization test passed")
        
    except Exception as e:
        print(f"\n✗ UI test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    test_ui_initialization()
