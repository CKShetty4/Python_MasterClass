# tests/test_Introducing_Artificial_Intelligence_System.py
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util
import os
import time
import tracemalloc
import ast

GREEN = "\033[92m"
RED   = "\033[91m"
YELLOW= "\033[93m"
RESET = "\033[0m"

# -----------------------------
# Template for skipping unchanged files
# -----------------------------
TEMPLATE_SOURCE = """'''
Objective:

To work with print statement

Problem Description:

Imagine yourself to be a scientist who has developed a intellectual  system that converts text to speech. You are getting ready for its demo and want to feed the information that your system has to convert to speech. Simulate this through python.
Note: The information includes the name of the AI system, creator, purpose of creation, Memory etc.  Refer the sample input and output statements for more clarifications.



Sample Input:
Enter the name: Software 2.0
Enter the creator name: XYZ
Enter the purpose: Conversion of Text to Speech
Enter the memory size: 500Gb
Enter the speed: 5.5

Sample Output:

My Details:
I am Software 2.0 , created by XYZ, for the purpose of Conversion of Text to Speech.
Memory I consume is around 500Gb and my speed is 5.5 GHZ.
'''
# Code Here

"""

STUDENT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..", "Introducing_Artificial_Intelligence_System",
    "Introducing_Artificial_Intelligence_System.py"
)

class TestAI(unittest.TestCase):
    """Test AI introduction program strictly."""

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(STUDENT_FILE):
            raise unittest.SkipTest(f"{RED}Student file not found. Skipping.{RESET}")
        with open(STUDENT_FILE, "r", encoding="utf-8") as f:
            student_src = f.read()
        if student_src.strip() == TEMPLATE_SOURCE.strip():
            raise unittest.SkipTest(f"{RED}Student has not changed the template. Skipping.{RESET}")

    def run_student_code(self):
        spec = importlib.util.spec_from_file_location("student_code", STUDENT_FILE)
        student = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student)
        return student

    def test_ai_output_and_single_print(self):
        test_inputs = ["Software 2.0", "XYZ", "Conversion of Text to Speech", "500Gb", "5.5"]
        expected_output = (
            "My Details: \n"
            "I am Software 2.0, created by XYZ, for the purpose of Conversion of Text to Speech.\n"
            "Memory I consume is around 500Gb and my speed is 5.5 GHZ.\n"
        )
        input_prompts = [
            "Enter the name: ",
            "Enter the creator name: ",
            "Enter the purpose: ",
            "Enter the memory size: ",
            "Enter the speed: "
        ]

        counter = {"i": 0}
        def input_mock(prompt=None):
            expected_prompt = input_prompts[counter["i"]]
            assert prompt == expected_prompt, \
                f"{RED}❌ input() prompt mismatch! Expected {expected_prompt!r}, got {prompt!r}{RESET}"
            val = test_inputs[counter["i"]]
            counter["i"] += 1
            return val

        with patch("builtins.input", side_effect=input_mock), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:

            tracemalloc.start()
            start = time.perf_counter()

            self.run_student_code()

            end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            output = mock_stdout.getvalue()
            self.assertEqual(
                output,
                expected_output,
                f"{RED}❌ Output mismatch!\nExpected: {expected_output!r}\nGot:      {output!r}{RESET}"
            )

            # Ensure exactly one print() is used
            with open(STUDENT_FILE, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            print_calls = [n for n in ast.walk(tree)
                           if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "print"]
            self.assertEqual(
                len(print_calls),
                1,
                f"{RED}❌ Student must use exactly one print() statement! Found {len(print_calls)}{RESET}"
            )

            print(YELLOW + f"Time: {end-start:.6f}s | Peak memory: {peak} bytes" + RESET)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAI)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(GREEN + "✅ All AI tests passed!" + RESET)
    else:
        print(RED + "❌ Some AI tests failed." + RESET)
