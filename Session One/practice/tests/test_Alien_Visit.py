# tests/test_Alien_Visit.py
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util
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
# Original starter code template for Alien_Visit.py
# ----------------------------------------------------------

TEMPLATE_SOURCE = """'''
Objective:

To work with the input and output statements

Problem Description:

Imagine that you are in a desert and all of a sudden, a space shuttle lands in front of you. An alien walks out of the space shuttle and greets you. Write a Python program to welcome this friendly alien to our planet - Earth.  Get the name of the alien from the user and display the welcome message as given in the sample output.

Sample Input:
Enter the name: Naoto

Sample Output:
Hello Naoto! Welcome to our planet Earth.

Guidelines:
Step 1: Get the name from the user and store it into a variable:
Step 2:  Concatenate the name with the string messages provided in the problem description and display it:
'''

#Code here

"""

# ----------------------------------------------------------
# Student file path
# ----------------------------------------------------------
STUDENT_FILE = os.path.join(os.path.dirname(__file__), "..", "Alien_Visit", "Alien_Visit.py")

# ----------------------------------------------------------
# Test case
# ----------------------------------------------------------
class TestAlienVisit(unittest.TestCase):
    """Verify Alien_Visit.py prints exact greeting and uses exact prompt."""

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(STUDENT_FILE):
            raise unittest.SkipTest(f"{RED}Student file not found. Skipping.{RESET}")

    def run_student_code(self):
        """Import and execute the student's script fresh each time."""
        spec = importlib.util.spec_from_file_location("student_code", STUDENT_FILE)
        student = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student)
        return student

    def test_greeting_for_multiple_names(self):
        test_names = ["Naoto", "Zara", "Ali", "Maya", "Leo"]

        for name in test_names:
            with self.subTest(name=name):
                # Use a side_effect to check the input prompt string
                def input_mock(prompt=None):
                    self.assertEqual(
                        prompt,
                        "Enter the name: ",
                        f"{RED}❌ input() prompt mismatch! Expected 'Enter the name:', got {prompt!r}{RESET}"
                    )
                    return name

                with patch("builtins.input", side_effect=input_mock), \
                     patch("sys.stdout", new_callable=StringIO) as mock_stdout:

                    # Measure time & memory
                    tracemalloc.start()
                    start = time.perf_counter()

                    self.run_student_code()

                    end = time.perf_counter()
                    _, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    output = mock_stdout.getvalue()
                    expected = f"Hello {name}! Welcome to our planet Earth.\n"

                    # STRICT output comparison
                    self.assertEqual(
                        output,
                        expected,
                        f"{RED}❌ Output mismatch for name '{name}'.\n"
                        f"Expected: {expected!r}\nGot:      {output!r}{RESET}"
                    )

                    # Print performance metrics
                    print(
                        YELLOW
                        + f"[{name}] Time: {end - start:.6f}s | Peak memory: {peak} bytes"
                        + RESET
                    )

# ----------------------------------------------------------
# CLI runner
# ----------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAlienVisit)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if result.wasSuccessful():
        print(GREEN + "✅ All Alien_Visit tests passed!" + RESET)
    else:
        print(RED + "❌ Some Alien_Visit tests failed!" + RESET)
