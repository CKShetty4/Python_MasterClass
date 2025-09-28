"""
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

"""

# Code Here
