"""
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
"""

# Code Here
