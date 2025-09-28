# tests/test_welcome_message.py
import unittest
from io import StringIO
from unittest.mock import patch
import importlib
import os
import time
import tracemalloc

# ----------------------------------------------------------
# ANSI colors
# ----------------------------------------------------------
GREEN = "\033[92m"
RED   = "\033[91m"
YELLOW= "\033[93m"
RESET = "\033[0m"

# ----------------------------------------------------------
# Original starter code (template)
# ----------------------------------------------------------
TEMPLATE_SOURCE = """'''
Objective:

To work with the print statement

Problem Description:

Write a python program to welcome your friends to the Data Science course.

Sample Output:
Welcome to Data Science Course!

Guidelines:
Step1: Print the welcome message provided in the problem description and display it 
'''

# Code here
"""

# ----------------------------------------------------------
# Student file path
# ----------------------------------------------------------
STUDENT_FILE = os.path.join(os.path.dirname(__file__), "..", "welcome_message", "welcome_message.py")

# ----------------------------------------------------------
# Test case
# ----------------------------------------------------------
class TestWelcomeMessage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(STUDENT_FILE):
            raise unittest.SkipTest(f"{RED}Student file not found. Skipping.{RESET}")

    @patch("sys.stdout", new_callable=StringIO)
    def test_welcome_output(self, mock_stdout):
        """Executes student script once and verifies exact output."""
        # Clear previous module import if exists (fresh run)
        module_name = "welcome_message.welcome_message"
        if module_name in importlib.sys.modules:
            del importlib.sys.modules[module_name]

        # Measure memory and time
        tracemalloc.start()
        start = time.perf_counter()

        importlib.import_module(module_name)  # runs student code ONCE

        end = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Capture stdout
        output = mock_stdout.getvalue()

        # Strict type check
        self.assertIsInstance(output, str, f"{RED}❌ Output is not a string{RESET}")

        # Exact match check (no whitespace tolerance)
        expected_output = "Welcome to Data Science Course!\n"
        self.assertEqual(
            output,
            expected_output,
            f"{RED}❌ Output mismatch!\nExpected: {expected_output!r}\nGot:      {output!r}{RESET}"
        )

        # Performance metrics
        print(YELLOW + f"[Performance] Time: {end - start:.6f}s | Peak memory: {peak} bytes" + RESET)


# ----------------------------------------------------------
# CLI runner
# ----------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWelcomeMessage)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if result.wasSuccessful():
        print(GREEN + "✅ All tests passed!" + RESET)
    else:
        print(RED + "❌ Some tests failed." + RESET)
