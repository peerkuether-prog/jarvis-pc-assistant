#!/usr/bin/env python
"""Run all tests for Jarvis Premium."""

import subprocess
import sys
from pathlib import Path

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
END = "\033[0m"


def run_test(test_file: str, description: str) -> bool:
    """Run a single test file and report results."""
    print(f"\n{BLUE}{'='*60}{END}")
    print(f"{BLUE}Running: {description}{END}")
    print(f"{BLUE}{'='*60}{END}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=False,
            timeout=60,
        )
        if result.returncode == 0:
            print(f"{GREEN}✓ {description} PASSED{END}")
            return True
        else:
            print(f"{RED}✗ {description} FAILED{END}")
            return False
    except subprocess.TimeoutExpired:
        print(f"{RED}✗ {description} TIMEOUT{END}")
        return False
    except Exception as e:
        print(f"{RED}✗ {description} ERROR: {e}{END}")
        return False


def main():
    """Run all test suites."""
    print(f"\n{YELLOW}{'='*60}{END}")
    print(f"{YELLOW}JARVIS PREMIUM TEST SUITE{END}")
    print(f"{YELLOW}{'='*60}{END}")
    
    tests_dir = Path(__file__).parent
    
    test_suite = [
        ("test_imports.py", "Import & Integrity Check"),
        ("test_commands.py", "Command Parsing Tests"),
        ("test_ui.py", "UI Initialization Test"),
        ("test_integration.py", "Full Integration Test"),
    ]
    
    results = []
    for test_file, description in test_suite:
        test_path = tests_dir / test_file
        if test_path.exists():
            passed = run_test(str(test_path), description)
            results.append((description, passed))
        else:
            print(f"{RED}✗ Test file not found: {test_file}{END}")
            results.append((description, False))
    
    # Summary
    print(f"\n{BLUE}{'='*60}{END}")
    print(f"{BLUE}TEST SUMMARY{END}")
    print(f"{BLUE}{'='*60}{END}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for description, passed in results:
        status = f"{GREEN}✓ PASS{END}" if passed else f"{RED}✗ FAIL{END}"
        print(f"{status} - {description}")
    
    print(f"\n{BLUE}Total: {passed_count}/{total_count} tests passed{END}")
    
    if passed_count == total_count:
        print(f"\n{GREEN}{'='*60}{END}")
        print(f"{GREEN}ALL TESTS PASSED ✓{END}")
        print(f"{GREEN}Jarvis Premium is ready for production!{END}")
        print(f"{GREEN}{'='*60}{END}")
        return 0
    else:
        print(f"\n{RED}{'='*60}{END}")
        print(f"{RED}SOME TESTS FAILED ✗{END}")
        print(f"{RED}{'='*60}{END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
