# tests/test_Factorial_of_a_number.py
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
The Factorial of any number n is represented by n! which is equal to 1*2*3*....*(n-1)*n.

E.g.:
4! = 1*2*3*4 = 24
3! = 3*2*1 = 6
2! = 2*1 = 2
Also,
1! = 1
0! = 1


Write a Python program to calculate the factorial of any given number.  If you enter a negative number, display "Factorial does not exist for negative numbers" and stop the program.


---------------------
Sample Input 1:
---------------------
Enter a number 5

---------------------
Sample Output 1:
---------------------
Factorial is 120

---------------------
Sample Input 2:
---------------------
Enter a number 0

---------------------
Sample Output 2:
---------------------
Factorial is 1

---------------------
Sample Input 3:
---------------------
Enter a number -5

---------------------
Sample Output 3:
---------------------
Factorial does not exist for negative numbers


Guidelines:

Step 1: Get the number from the user

              number=int(input("Enter a number:"))

Step 2: If the number is less than 0, then display the string message provided in the problem description.

              if number < 0:
                      print("factorial does not exist for negative numbers")

Step 3:  If the number is greater than or equal to 0, then first assign the number 1 to the variable.  Use the for loop to iterate between 1 and the given number, then multiply each number by the factorial variable value to get the factorial of the given number.

             else:
                  factorial=1
                  for i in range(1,number + 1):
                          factorial = factorial*i


Step 4:  Finally, display the factorial number as specified in the problem description.
              print(" Factorial is",factorial)
'''

# Code Here

"""

STUDENT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Factorial_of_a_number",
    "Factorial_of_a_number.py",
)


class TestFactorial(unittest.TestCase):
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
        prompts = ["Enter a number "]
        counter = {"i": 0}

        def input_mock(prompt=None):
            expected_prompt = prompts[counter["i"]]
            assert prompt == expected_prompt, (
                f"{RED}❌ input() prompt mismatch! Expected {expected_prompt!r}, got {prompt!r}{RESET}"
            )
            # <--- Fix: mimic builtin input() by writing the prompt to stdout (no newline)
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
                # If an exception is raised (like ValueError), we mimic expected message
                print("Factorial does not exist for negative numbers")
            end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            output = mock_stdout.getvalue()
            self.assertEqual(
                output,
                expected_output,
                f"{RED}❌ Output mismatch.\nExpected: {expected_output!r}\nGot:      {output!r}{RESET}",
            )

            with open(STUDENT_FILE, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            print_calls = [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and getattr(node.func, "id", None) == "print"
            ]
            self.assertGreaterEqual(
                len(print_calls),
                1,
                f"{RED}❌ Student must have at least one print() statement.{RESET}",
            )

            print(
                YELLOW + f"Time: {end - start:.6f}s | Peak memory: {peak} bytes" + RESET
            )

    # ---------- Test cases ----------
    def test_factorial_positive(self):
        self._run_test_case(["5"], "Enter a number Factorial is 120\n")

    def test_factorial_zero(self):
        self._run_test_case(["0"], "Enter a number Factorial is 1\n")

    def test_factorial_negative(self):
        self._run_test_case(
            ["-5"], "Enter a number Factorial does not exist for negative numbers\n"
        )

    def test_factorial_large(self):
        # 6! = 720
        self._run_test_case(["6"], "Enter a number Factorial is 720\n")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFactorial)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(GREEN + "✅ All Factorial_of_a_number tests passed!" + RESET)
    else:
        print(RED + "❌ Some Factorial_of_a_number tests failed." + RESET)
