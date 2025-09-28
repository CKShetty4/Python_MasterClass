# tests/test_Vaccine_Details.py
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
To work with conditional and looping statements

Problem Description:

The state committee announced that all people should get vaccinated against corona-19. So the state's area counselor wanted to know the number of non-vaccinated people in his area, as well as the percentage of people who have received two doses of vaccine.

Write a Python program that helps the counselor get the details of vaccinated and non-vaccinated people. Refer to the sample input and output statements for more clarification.



Note:

- If the total number of people in the area is less than or equal to 0, then it displays the message "Invalid input" and terminates the program.
- If the single-dose count is less than 0 or greater than the total number of people count, then display the message "Invalid input" and terminate the program.
- If the double dose count is less than 0 or greater than the total number of people count, then display the message "Invalid Input" and terminate the program.
- If single and double dose total counts are greater than the total area count, then it should display the message "Invalid Input" and terminate the program.
- If the councilor needs to collect details of the next area, then he needs to press  "1", else press " 0" to terminate the program.
- If he enters anything other than '0' or '1', it should display the message as "Invalid Input" and terminate the program.
- Use the 'break' statement to terminate the program.
- Total vaccinated percentage of people should be calcualted by (double dose count/total no of people)*100

----------------------------------------
Sample Input and output statement 1:
----------------------------------------

Enter the total no of people in the area: 60
Single-dose count: 20
Double-dose count: 40
Not vaccinated people count: 0
Total vaccinated percentage of people: 66.67
Do you want to continue (1) for yes (0) for no: 1
Enter the total no of people in the area: 50
Single-dose count: 27
Double-dose count: 20
Not vaccinated people count: 3
Total vaccinated percentage of people: 40.00
Do you want to continue (1) for yes (0) for no: 0

----------------------------------------
Sample Input and output statement 2:
----------------------------------------

Enter the total no of people in the area: -3
Invalid Input

----------------------------------------
Sample Input and output statement 3:
----------------------------------------
Enter the total no of people in the area: 30
Single-dose count: 5
Double-dose count: 35
Invalid Input

----------------------------------------
Sample Input and output statement 4:
----------------------------------------

Enter the total no of people in the area: 30
Single-dose count: 5
Double-dose count: 28
Invalid Input

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
    "Vaccine_Details",
    "Vaccine_Details.py",
)


class TestVaccineDetails(unittest.TestCase):
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
        # This program loops; we prompt each time
        # after each area processed until continue == 0 or invalid input
        prompts = [
            "Enter the total no of people in the area: ",
            "Single-dose count: ",
            "Double-dose count: ",
            "Do you want to continue (1) for yes (0) for no: ",
        ]
        counter = {"i": 0}

        def input_mock(prompt=None):
            # cycle prompts, repeating after each continue == 1
            expected_prompt = prompts[counter["i"] % 4]
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
                print("Invalid Input")
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
    def test_valid_two_areas(self):
        self._run_test_case(
            ["60", "20", "40", "1", "50", "27", "20", "0"],
            "Not vaccinated people count: 0\nTotal vaccinated percentage of people: 66.67\n"
            "Not vaccinated people count: 3\nTotal vaccinated percentage of people: 40.00\n",
        )

    def test_invalid_total_people_zero(self):
        self._run_test_case(["0"], "Invalid Input\n")

    def test_invalid_total_people_negative(self):
        self._run_test_case(["-3"], "Invalid Input\n")

    def test_invalid_single_dose_negative(self):
        self._run_test_case(["30", "-5"], "Invalid Input\n")

    def test_invalid_single_dose_exceeds_total(self):
        self._run_test_case(["30", "35"], "Invalid Input\n")

    def test_invalid_double_dose_negative(self):
        self._run_test_case(["30", "5", "-10"], "Invalid Input\n")

    def test_invalid_double_dose_exceeds_total(self):
        self._run_test_case(["30", "5", "35"], "Invalid Input\n")

    def test_invalid_sum_exceeds_total(self):
        self._run_test_case(["30", "5", "28"], "Invalid Input\n")

    def test_continue_invalid_input_char(self):
        self._run_test_case(
            ["40", "10", "20", "2"],  # invalid continue value
            "Not vaccinated people count: 10\nTotal vaccinated percentage of people: 50.00\nInvalid Input\n",
        )

    def test_continue_invalid_input_text(self):
        self._run_test_case(
            ["40", "10", "20", "yes"],
            "Not vaccinated people count: 10\nTotal vaccinated percentage of people: 50.00\nInvalid Input\n",
        )

    def test_zero_vaccinated(self):
        self._run_test_case(
            ["100", "0", "0", "0"],
            "Not vaccinated people count: 100\nTotal vaccinated percentage of people: 0.00\n",
        )

    def test_all_double_dose(self):
        self._run_test_case(
            ["80", "0", "80", "0"],
            "Not vaccinated people count: 0\nTotal vaccinated percentage of people: 100.00\n",
        )

    def test_all_single_dose(self):
        self._run_test_case(
            ["50", "50", "0", "0"],
            "Not vaccinated people count: 0\nTotal vaccinated percentage of people: 0.00\n",
        )

    def test_fractions_percentage(self):
        self._run_test_case(
            ["30", "5", "7", "0"],
            "Not vaccinated people count: 18\nTotal vaccinated percentage of people: 23.33\n",
        )


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVaccineDetails)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(GREEN + "✅ All Vaccine_Details tests passed!" + RESET)
    else:
        print(RED + "❌ Some Vaccine_Details tests failed." + RESET)
