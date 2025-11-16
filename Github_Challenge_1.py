x = float(input("Enter the first number - "))
y = float(input("Enter the second number - "))

addition = x+y
substraction = x - y
multiplication = x*y
if x != 0:
    division = x/y
else:
    print("Cannot divide a number by zero")

print("The sum of the above two numbers is = ", addition)
print("The difference of the above two numbers is = ", substraction)
print("The product of the above two numbers is = ", multiplication)
print("The division of the above two numbers is = ", division)