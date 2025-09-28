# tests/test_Armstrong_Number.py
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util
import os
import time
import tracemalloc
import ast

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

TEMPLATE_SOURCE = """'''
Objective:
To work with Control structures

Problem Description:

If the sum of the cubes of  the digits in a three-digit number is equal to the number itself, then the number is called an Armstrong number.
E.g.: 153 is an Armstrong number because (1^3)+(5^3)+(3^3) = 153.
Write a program in Python to display all the  Armstrong numbers between n1 and n2.

Guidelines:

- If the starting and ending numbers are negative then display the message "Starting and ending numbers must be greater than or equal to zero" and stop the program.
- If the starting number is greater than the ending number, then display the message "Invalid input!! Ending number should be greater than starting number" and stop the program.
- Refer to the sample input and output statements for more clarifications.
To get multiple input values in a single input(), use the below mentioned approach:
 n1,n2=map(int,input("Enter the starting and ending numbers:\n").split(" "))

-------------------------------
Sample Input 1:
-------------------------------
Enter the starting and ending numbers:
5 500
-------------------------------
Sample Output 1:
-------------------------------
Armstrong numbers between 5 and 500 are:
153
370
371
407

-------------------------------
Sample Input 2:
-------------------------------
Enter the starting and ending numbers:
50 100

-------------------------------
Sample Output 2:
-------------------------------
Armstrong numbers between 50 and 100 are:
There is no Armstrong number between these numbers

-------------------------------
Sample Input 3:
-------------------------------
Enter the starting and ending numbers:
1 10

-------------------------------
Sample Output 3:
-------------------------------
Armstrong numbers between 1 and 10 are:
1

-------------------------------
Sample Input 4:
-------------------------------
Enter the starting and ending numbers:
-4 2

-------------------------------
Sample Output 4:
-------------------------------
Starting and ending numbers must be greater than or equal to zero


-------------------------------
Sample Input 5:
-------------------------------
Enter the starting and ending numbers:
100 6

-------------------------------
Sample Output 5:
-------------------------------
Invalid input!! Ending number should be greater than starting number

'''
# Do not change the proivided Code skeleton


def main():
    # Code here

    return


main()
"""

STUDENT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Armstrong_Number",
    "Armstrong_Number.py",
)


class TestArmstrong(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(STUDENT_FILE):
            raise unittest.SkipTest(f"{RED}Student file not found. Skipping.{RESET}")
        with open(STUDENT_FILE, "r", encoding="utf-8") as f:
            src = f.read()
        if src.strip() == TEMPLATE_SOURCE.strip():
            raise unittest.SkipTest(
                f"{RED}Student has not changed the template. Skipping.{RESET}"
            )

    def run_student_code(self):
        spec = importlib.util.spec_from_file_location("student_code", STUDENT_FILE)
        student = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student)
        return student

    def _run_test_case(self, inputs, expected_output):
        prompts = ["Enter the starting and ending numbers:\n"]
        counter = {"i": 0}

        def input_mock(prompt=None):
            expected_prompt = prompts[counter["i"]]
            assert prompt == expected_prompt, (
                f"{RED}❌ input() prompt mismatch! Expected {expected_prompt!r}, got {prompt!r}{RESET}"
            )
            # Mimic real input(): print the prompt (without extra newline)
            print(expected_prompt, end="")
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
            except Exception:
                raise
            end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            output = mock_stdout.getvalue()
            self.assertEqual(
                output,
                expected_output,
                f"{RED}❌ Output mismatch.\nExpected: {expected_output!r}\nGot:      {output!r}{RESET}",
            )

            # Ensure at least one print statement
            with open(STUDENT_FILE, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            print_calls = [
                n
                for n in ast.walk(tree)
                if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "print"
            ]
            self.assertGreaterEqual(
                len(print_calls),
                1,
                f"{RED}❌ Student must have at least one print() statement.{RESET}",
            )

            print(
                YELLOW + f"Time: {end - start:.6f}s | Peak memory: {peak} bytes" + RESET
            )

    # ---------------- TEST CASES ----------------
    def test_case1_valid_range(self):
        expected = (
            "Enter the starting and ending numbers:\n"
            "Armstrong numbers between 5 and 500 are:\n"
            "153\n370\n371\n407\n"
        )
        self._run_test_case(["5 500"], expected)

    def test_case2_no_armstrong(self):
        expected = (
            "Enter the starting and ending numbers:\n"
            "Armstrong numbers between 50 and 100 are:\n"
            "There is no Armstrong number between these numbers\n"
        )
        self._run_test_case(["50 100"], expected)

    def test_case3_single_digit(self):
        expected = (
            "Enter the starting and ending numbers:\n"
            "Armstrong numbers between 1 and 10 are:\n"
            "1\n"
        )
        self._run_test_case(["1 10"], expected)

    def test_case4_negative_input(self):
        expected = (
            "Enter the starting and ending numbers:\n"
            "Starting and ending numbers must be greater than or equal to zero\n"
        )
        self._run_test_case(["-4 2"], expected)

    def test_case5_start_greater_than_end(self):
        expected = (
            "Enter the starting and ending numbers:\n"
            "Invalid input!! Ending number should be greater than starting number\n"
        )
        self._run_test_case(["100 6"], expected)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestArmstrong)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(GREEN + "✅ All Armstrong_Number tests passed!" + RESET)
    else:
        print(RED + "❌ Some Armstrong_Number tests failed." + RESET)
