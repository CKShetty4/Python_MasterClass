# tests/test_Stationary_Shop.py
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
Ojective:
To work with Operators

Scenario:
A new stationary shop has been opened in the city. The owner asks his accountant to take the list of items sold in the store. The list should contain the details of the items and their costs. Help the accountant to generate the price list by writing a Python program.

Get the price of the items from the user and generate a list with 4 products - A4 sheets, pens, pencils, and erasers.  Also, the program should display the total cost of all the products.

Please refer to the sample input and output statements for more clarifications.

Guidelines:

The amount must be displayed with 2 decimal places.

--------------------------
Sample Input 1 :
--------------------------
Cost of A4sheet: 40.0
Cost of pen: 20.0
Cost of pencil: 10.0
Cost of eraser: 5.0

--------------------------
Sample Output 1 :
--------------------------
Items Details
A4sheet: 40.00
Pen: 20.00
Pencil: 10.00
Eraser: 5.00
Total cost: 75.00

--------------------------
Sample Input 2 :
--------------------------
Cost of A4sheet: -20.0

-------------------------
Sample Output 2:
-------------------------
Invalid input

'''
# Code Here
"""

STUDENT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Stationary_Shop",
    "Stationary_Shop.py",
)


class TestStationaryShop(unittest.TestCase):
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
        prompts = [
            "Cost of A4sheet: ",
            "Cost of pen: ",
            "Cost of pencil: ",
            "Cost of eraser: ",
        ]
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
            except Exception:
                # Any exception is treated as invalid input
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

            # Count only print calls for final output
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
    def test_valid_input(self):
        self._run_test_case(
            ["40", "20", "10", "5"],
            "Items Details\nA4sheet: 40.00\nPen: 20.00\nPencil: 10.00\nEraser: 5.00\nTotal cost: 75.00\n",
        )

    def test_valid_input2(self):
        self._run_test_case(
            ["44", "20.0", "10", "15.8"],
            "Items Details\nA4sheet: 44.00\nPen: 20.00\nPencil: 10.00\nEraser: 15.80\nTotal cost: 89.80\n",
        )

    def test_float_input(self):
        self._run_test_case(
            ["40.5", "20.25", "10.75", "5.0"],
            "Items Details\nA4sheet: 40.50\nPen: 20.25\nPencil: 10.75\nEraser: 5.00\nTotal cost: 76.50\n",
        )

    def test_zero_values(self):
        self._run_test_case(
            ["0", "0", "0", "0"],
            "Items Details\nA4sheet: 0.00\nPen: 0.00\nPencil: 0.00\nEraser: 0.00\nTotal cost: 0.00\n",
        )

    def test_negative_input(self):
        self._run_test_case(["-40", "20", "10", "5"], "Invalid input\n")

    def test_negative_input2(self):
        self._run_test_case(["40", "-20", "10", "5"], "Invalid input\n")

    def test_negative_input3(self):
        self._run_test_case(["40", "20", "-10", "5"], "Invalid input\n")

    def test_non_numeric_input(self):
        self._run_test_case(["abc", "20", "10", "5"], "Invalid input\n")

    def test_partial_invalid_input(self):
        self._run_test_case(["40", "20", "xyz", "5"], "Invalid input\n")

    def test_negative_late_input(self):
        self._run_test_case(["40", "20", "10", "-5"], "Invalid input\n")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStationaryShop)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(GREEN + "✅ All Stationary_Shop tests passed!" + RESET)
    else:
        print(RED + "❌ Some Stationary_Shop tests failed." + RESET)
