# tests/test_Window_seat_or_not.py
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

Renn plans a trip to Goa, this weekend. He decides to go by bus and book his ticket through a website. Code logic in Python so that he gets to know if he has booked a window seat or not.

Assume the bus to have 11 rows.  Seat number begins with 1 which will be a window seat.  If the no. of seats per row is a factor of the seat number you have entered, then it is a window seat, else it is not a window seat.   Refer to the sample input and output statements for more clarifications.

Guidelines:
1. For any invalid seat number specified is a negative number, zero or the seat number is greater than total no. of seats, then display - "Invalid Seat Number" and stop the program.

2. If the no. of seats per row specified is less than or equal to zero, then display - "Invalid Input" and stop the program.

---------------------
Sample Input 1:
---------------------
Enter the number of seats per row
4
Enter the seat number
36

---------------------
Sample Output 1:
---------------------
Window Seat

---------------------
Sample Input 2:
---------------------
Enter the number of seats per row
3
Enter the seat number
20

---------------------
Sample Output 2:
---------------------
Not a Window Seat

---------------------
Sample Input 3:
---------------------
Enter the number of seats per row
4
Enter the seat number
48

---------------------
Sample Output 3:
---------------------
Invalid Seat Number

'''
# Do not change the proivided Code skeleton


def check_window_seat():
    # Code here

    return


check_window_seat()
"""

STUDENT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Window_seat_or_not",
    "Window_seat_or_not.py",
)


class TestWindowSeat(unittest.TestCase):
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
        # expected prompts
        prompts = ["Enter the number of seats per row\n", "Enter the seat number\n"]
        counter = {"i": 0}

        def input_mock(prompt=None):
            expected_prompt = prompts[counter["i"]]
            assert prompt == expected_prompt, (
                f"{RED}❌ input() prompt mismatch! Expected {expected_prompt!r}, got {prompt!r}{RESET}"
            )
            # mimic built-in input(): print prompt to stdout (no extra newline)
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

            # ensure at least one print() exists
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

    # ------------------ TEST CASES ------------------
    def test_window_seat(self):
        expected = (
            "Enter the number of seats per row\nEnter the seat number\nWindow Seat\n"
        )
        # seats_per_row = 4, seat_number = 36  → window seat
        self._run_test_case(["4", "36"], expected)

    def test_not_window_seat(self):
        expected = (
            "Enter the number of seats per row\n"
            "Enter the seat number\n"
            "Not a Window Seat\n"
        )
        # seats_per_row = 3, seat_number = 20  → not window
        self._run_test_case(["3", "20"], expected)

    def test_invalid_seat_number_too_high(self):
        expected = (
            "Enter the number of seats per row\n"
            "Enter the seat number\n"
            "Invalid Seat Number\n"
        )
        # seats_per_row = 4 → total seats = 44 → seat 48 invalid
        self._run_test_case(["4", "48"], expected)

    def test_invalid_seat_number_negative(self):
        expected = (
            "Enter the number of seats per row\n"
            "Enter the seat number\n"
            "Invalid Seat Number\n"
        )
        self._run_test_case(["4", "-2"], expected)

    def test_invalid_seat_number_zero(self):
        expected = (
            "Enter the number of seats per row\n"
            "Enter the seat number\n"
            "Invalid Seat Number\n"
        )
        self._run_test_case(["4", "0"], expected)

    def test_invalid_input_zero_seats(self):
        expected = (
            "Enter the number of seats per row\nEnter the seat number\nInvalid Input\n"
        )
        # seats_per_row <= 0 → invalid input
        self._run_test_case(["0", "10"], expected)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWindowSeat)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(GREEN + "✅ All Window_seat_or_not tests passed!" + RESET)
    else:
        print(RED + "❌ Some Window_seat_or_not tests failed." + RESET)
