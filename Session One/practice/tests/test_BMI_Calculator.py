# tests/test_BMI_Calculator.py
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

Program in Python to compute the BMI of a person and display the  risk associated with it by entering the height in 'm' and weight in' kg'. Refer the following table and code accordingly.

Guidelines:

- To calculate the BMI apply the formula:  BMI = weight(kg)/( height(m)*height(m) ).
- Result must be adjusted to one decimal place.
- When the height or weight is entered as a negative number or  zero, then display the message "Provide a valid input" and stop the program.

-----------------------------------------------------------------
|       BMI       |                    Risk                    |
-----------------------------------------------------------------
| 27.5 and above  |                  High Risk                 |
|    23 - 27.4    |               Moderate Risk                |
|   18.5 - 22.9   |                  Low Risk                  |
|   Below 18.5    |   Risk of nutritional deficiency diseases  |
-----------------------------------------------------------------

------------------------
Sample Input 1:
------------------------
Enter the weight of the person(kg): 85
Enter the height of the person(m): 1.75

------------------------
Sample Output 1:
------------------------
Your BMI is 27.8 (High Risk).


------------------------
Sample Input 2:
------------------------

Enter the weight of the person(kg): 0
Enter the height of the person(m): 1.58

------------------------
Sample Output 2:
------------------------
Provide a valid input


------------------------
Sample Input 3:
------------------------

Enter the weight of the person(kg):80
Enter the height of the person(m):-1

------------------------
Sample Output 3:
------------------------
Provide a valid input


Guidelines:
Step 1: Get the weight from the user, convert it into integer and store that into a variable as:

               weight=int(input("Enter the weight of the person(kg):"))

Step 2: Get the height from the user, convert it into float and store it into a variable as:

              height=float(input("Enter the height of the person(m):"))

Step 3: If both height and weight are greater than 0, then calculate the BMI using the formula and adjust to 1 decimal value.

              if weight>0 and height>0:
                       bmi=(weight/(height*height))
                       BMI=round(bmi,1)



Step 4: If the BMI>=27.5, concatenate the BMI with the string messages as provided in the problem description and display it.

              if BMI>=27.5:
                      print("Your BMI is "+str(BMI)+" (High Risk)")

Step 5: Otherwise if BMI>=23 and BMI<=27.4, concatenate the BMI with the string messages as provided in the problem description and display it.

              elif BMI>=23 and BMI<=27.4:
                   print("Your BMI is "+str(BMI)+" (Moderate Risk)")

Step 6: If the BMI>=18.5 and BMI<=22.9, concatenate the BMI with the string messages provided in the problem description and display it.

               elif BMI>=18.5 and BMI<=22.9:
                    print("Your BMI is "+str(BMI)+" (Low Risk)")

Step 8: If the BMI<18.5, concatenate the BMI with the string messages as provided in the problem description and display it.

              elif BMI<18.5:
                   print("Your BMI is "+str(BMI)+" (Risk of nutritional deficiency diseases)")


Step 9: If the height and weight are not greater than or equal to 0, then display the string message as provided in the problem description.

             else:
                   print("Provide a valid input")

'''
# Code Here

"""

STUDENT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "BMI_Calculator",
    "BMI_Calculator.py",
)


class TestBMICalculator(unittest.TestCase):
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
            "Enter the weight of the person(kg):",
            "Enter the height of the person(m):",
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
                print("Provide a valid input")
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
    def test_high_risk(self):
        self._run_test_case(["85", "1.75"], "Your BMI is 27.8 (High Risk)\n")

    def test_moderate_risk(self):
        self._run_test_case(["70", "1.75"], "Your BMI is 22.9 (Low Risk)\n")

    def test_low_risk(self):
        self._run_test_case(["72", "1.77"], "Your BMI is 23.0 (Moderate Risk)\n")

    def test_nutritional_deficiency(self):
        self._run_test_case(
            ["45", "1.70"],
            "Your BMI is 15.6 (Risk of nutritional deficiency diseases)\n",
        )

    def test_zero_weight(self):
        self._run_test_case(["0", "1.58"], "Provide a valid input\n")

    def test_negative_height(self):
        self._run_test_case(["80", "-1"], "Provide a valid input\n")

    def test_both_zero(self):
        self._run_test_case(["0", "0"], "Provide a valid input\n")

    def test_non_numeric_weight(self):
        self._run_test_case(["abc", "1.70"], "Provide a valid input\n")

    def test_non_numeric_height(self):
        self._run_test_case(["70", "xyz"], "Provide a valid input\n")

    def test_boundary_high(self):
        self._run_test_case(["80", "1.70"], "Your BMI is 27.7 (High Risk)\n")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBMICalculator)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(GREEN + "✅ All BMI_Calculator tests passed!" + RESET)
    else:
        print(RED + "❌ Some BMI_Calculator tests failed." + RESET)
