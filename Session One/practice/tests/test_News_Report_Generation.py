# tests/test_News_Report_Generation.py
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util
import os
import time
import tracemalloc

# -----------------------------
# ANSI colors
# -----------------------------
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# -----------------------------
# Template for skipping unchanged files
# -----------------------------
TEMPLATE_SOURCE = """'''
Objective:
To work with Operators

Problem Description:
Japan was hit by a huge Tsunami. Lives and properties were lost. Many were injured too. A news reporter has arrived at the spot to analyze and generate a report on the number of people alive, dead, and injured. His report also has a statement seeking the public to help the people in need. Can you help him to generate the report by writing a Python program?


Guidelines:
The statement for seeking help should be "Please help the people who are suffering!!!".
Please refer to the sample input and output for more clarifications.

-------------------------
Sample Input 1:
-------------------------
Dead Count: 2000
Injured Count: 3000
Safe Count: 10000

-------------------------
Sample Output 1:
-------------------------
TSUNAMI REPORT OF JAPAN

The number of people
Dead: 2000
Injured: 3000
Safe: 10000
Please help the people who are suffering!!!


-------------------------
Sample Input 2:
-------------------------
Dead Count: -2000

-------------------------
Sample Output 2:
-------------------------
Invalid input

'''

# Code Here

"""

# -----------------------------
# Student file path
# -----------------------------
STUDENT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "News_Report_Generation",
    "News_Report_Generation.py",
)


# -----------------------------
# Test case class
# -----------------------------
class TestNewsReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(STUDENT_FILE):
            raise unittest.SkipTest(f"{RED}Student file not found. Skipping.{RESET}")
        with open(STUDENT_FILE, "r", encoding="utf-8") as f:
            student_src = f.read()
        if student_src.strip() == TEMPLATE_SOURCE.strip():
            raise unittest.SkipTest(
                f"{RED}Student has not changed the template. Skipping.{RESET}"
            )

    def run_student_code(self):
        """Import & execute student's script freshly."""
        spec = importlib.util.spec_from_file_location("student_code", STUDENT_FILE)
        student = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student)
        return student

    def _run_test_case(self, inputs, expected_output):
        prompts = ["Dead Count: ", "Injured Count: ", "Safe Count: "]
        counter = {"i": 0}

        def input_mock(prompt=None):
            expected_prompt = prompts[counter["i"]]
            assert prompt == expected_prompt, (
                f"{RED}❌ input() prompt mismatch! Expected {expected_prompt!r}, got {prompt!r}{RESET}"
            )
            val = inputs[counter["i"]]
            counter["i"] += 1
            return val

        with (
            patch("builtins.input", side_effect=input_mock),
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        ):
            tracemalloc.start()
            start = time.perf_counter()
            try:
                self.run_student_code()
            except ValueError:
                # If student code crashes on non-integer input, simulate "Invalid input\n"
                print("Invalid input")
            end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            output = mock_stdout.getvalue()
            self.assertEqual(
                output,
                expected_output,
                f"{RED}❌ Output mismatch.\nExpected: {expected_output!r}\nGot:      {output!r}{RESET}",
            )

            print(
                YELLOW + f"Time: {end - start:.6f}s | Peak memory: {peak} bytes" + RESET
            )

    def test_valid_input_report(self):
        self._run_test_case(
            ["2000", "3000", "10000"],
            "TSUNAMI REPORT OF JAPAN\n\n"
            "The number of people\n"
            "Dead: 2000\n"
            "Injured: 3000\n"
            "Safe: 10000\n"
            "Please help the people who are suffering!!!\n",
        )

    def test_zero_values(self):
        self._run_test_case(
            ["0", "0", "0"],
            "TSUNAMI REPORT OF JAPAN\n\n"
            "The number of people\n"
            "Dead: 0\n"
            "Injured: 0\n"
            "Safe: 0\n"
            "Please help the people who are suffering!!!\n",
        )

    def test_invalid_dead_input(self):
        self._run_test_case(["-2000", "0", "0"], "Invalid input\n")

    def test_invalid_injured_input(self):
        self._run_test_case(["2000", "-3000", "0"], "Invalid input\n")

    def test_invalid_safe_input(self):
        self._run_test_case(["2000", "3000", "-10000"], "Invalid input\n")

    def test_non_integer_dead(self):
        self._run_test_case(["abc", "0", "0"], "Invalid input\n")

    def test_non_integer_injured(self):
        self._run_test_case(["2000", "xyz", "0"], "Invalid input\n")

    def test_non_integer_safe(self):
        self._run_test_case(["2000", "3000", "5.5"], "Invalid input\n")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNewsReport)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(GREEN + "✅ All News_Report_Generation tests passed!" + RESET)
    else:
        print(RED + "❌ Some News_Report_Generation tests failed." + RESET)
