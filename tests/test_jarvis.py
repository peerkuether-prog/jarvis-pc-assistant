import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from jarvis_app.system_tools import (
    safe_execute,
    open_app,
    open_url,
    list_dir,
    read_file,
    write_file,
    delete_file,
    get_system_summary,
    search_web,
    get_file_info,
)
from jarvis_app.voice import get_current_time, get_current_date, get_current_datetime
from jarvis_app.config import get_api_key, get_home_dir, get_config_dir


class TestSystemTools:
    """Test system tool functions."""

    def test_get_current_time(self):
        """Test time retrieval."""
        time_str = get_current_time()
        assert isinstance(time_str, str)
        assert len(time_str) > 0
        assert ":" in time_str

    def test_get_current_date(self):
        """Test date retrieval."""
        date_str = get_current_date()
        assert isinstance(date_str, str)
        assert len(date_str) > 0

    def test_get_current_datetime(self):
        """Test datetime retrieval."""
        dt_str = get_current_datetime()
        assert isinstance(dt_str, str)
        assert len(dt_str) > 0

    def test_get_system_summary(self):
        """Test system info retrieval."""
        summary = get_system_summary()
        assert isinstance(summary, str)
        assert "System:" in summary

    def test_safe_execute_empty_command(self):
        """Test safe_execute with empty command."""
        result = safe_execute("")
        assert "No command" in result

    def test_safe_execute_blocked_command(self):
        """Test safe_execute blocks dangerous commands."""
        result = safe_execute("del somefile.txt")
        assert "blocked" in result.lower()

    def test_open_url(self):
        """Test URL opening (doesn't actually open browser in test)."""
        result = open_url("https://google.com")
        assert "Opening" in result

    def test_open_url_no_protocol(self):
        """Test URL without protocol gets https added."""
        result = open_url("google.com")
        assert "Opening" in result

    def test_list_dir_home(self):
        """Test directory listing."""
        result = list_dir(get_home_dir())
        assert isinstance(result, str)
        assert len(result) > 0

    def test_list_dir_nonexistent(self):
        """Test directory listing with nonexistent path."""
        result = list_dir("/nonexistent/path/12345")
        assert "does not exist" in result

    def test_write_and_read_file(self):
        """Test writing and reading a file."""
        test_path = Path(get_home_dir()) / "test_jarvis.txt"
        test_content = "Hello, Jarvis test!"
        
        # Write file
        write_result = write_file(str(test_path), test_content)
        assert "written successfully" in write_result
        
        # Read file
        read_result = read_file(str(test_path))
        assert test_content in read_result
        
        # Cleanup
        delete_file(str(test_path))

    def test_delete_file(self):
        """Test file deletion."""
        test_path = Path(get_home_dir()) / "test_delete.txt"
        write_file(str(test_path), "temp")
        result = delete_file(str(test_path))
        assert "deleted" in result

    def test_delete_nonexistent_file(self):
        """Test deleting nonexistent file."""
        result = delete_file("/nonexistent/file.txt")
        assert "does not exist" in result

    def test_get_file_info(self):
        """Test getting file information."""
        test_path = Path(get_home_dir()) / "test_info.txt"
        write_file(str(test_path), "test content")
        result = get_file_info(str(test_path))
        assert "File:" in result or "test_info.txt" in result
        delete_file(str(test_path))

    def test_config_functions(self):
        """Test configuration functions."""
        home = get_home_dir()
        assert isinstance(home, str)
        assert len(home) > 0
        
        config_dir = get_config_dir()
        assert config_dir.exists()


class TestAssistant:
    """Test the main assistant functionality."""

    def test_assistant_init(self):
        """Test assistant initialization."""
        from jarvis_app.assistant import JarvisAssistant
        assistant = JarvisAssistant()
        assert assistant is not None
        assert hasattr(assistant, 'handle')
        assert hasattr(assistant, 'coding')
        assert hasattr(assistant, 'voice')

    def test_assistant_handle_empty(self):
        """Test assistant with empty input."""
        from jarvis_app.assistant import JarvisAssistant
        assistant = JarvisAssistant()
        result = assistant.handle("")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_assistant_handle_greeting(self):
        """Test assistant with greeting."""
        from jarvis_app.assistant import JarvisAssistant
        assistant = JarvisAssistant()
        result = assistant.handle("hello")
        assert "Hello" in result or "Jarvis" in result

    def test_assistant_handle_help(self):
        """Test assistant help command."""
        from jarvis_app.assistant import JarvisAssistant
        assistant = JarvisAssistant()
        result = assistant.handle("help")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_assistant_handle_time(self):
        """Test assistant time command."""
        from jarvis_app.assistant import JarvisAssistant
        assistant = JarvisAssistant()
        result = assistant.handle("what time is it")
        assert "time" in result.lower() or ":" in result

    def test_assistant_handle_date(self):
        """Test assistant date command."""
        from jarvis_app.assistant import JarvisAssistant
        assistant = JarvisAssistant()
        result = assistant.handle("what is today's date")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_assistant_handle_system(self):
        """Test assistant system info command."""
        from jarvis_app.assistant import JarvisAssistant
        assistant = JarvisAssistant()
        result = assistant.handle("system info")
        assert "System" in result

    def test_assistant_handle_blocked_command(self):
        """Test assistant blocks dangerous commands."""
        from jarvis_app.assistant import JarvisAssistant
        assistant = JarvisAssistant()
        result = assistant.handle("shutdown")
        assert "destructive" in result.lower() or "cannot" in result.lower()

    def test_assistant_log_action(self):
        """Test assistant logging."""
        from jarvis_app.assistant import JarvisAssistant
        assistant = JarvisAssistant()
        assistant.log_action("test input", "test response")
        assert len(assistant.history) == 1
        assert assistant.history[0]["user"] == "test input"
        assert assistant.history[0]["jarvis"] == "test response"


class TestAIClient:
    """Test the AI client."""

    def test_ai_client_init(self):
        """Test AI client initialization."""
        from jarvis_app.ai_client import AIClient
        client = AIClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.model is not None

    def test_coding_ai_init(self):
        """Test coding AI initialization."""
        from jarvis_app.assistant import CodingAI
        coding = CodingAI(api_key="test-key")
        assert coding.ai is not None
        assert hasattr(coding, 'review_code')
        assert hasattr(coding, 'generate_code')
        assert hasattr(coding, 'debug')
        assert hasattr(coding, 'explain')
        assert hasattr(coding, 'refactor')


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
