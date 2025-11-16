l1 = []
count = int(input("How many numbers do you want to enter? "))

for i in range(count):
    num = int(input("Enter a number: "))
    l1.append(num)

print("The entered list is - ",l1 )

reversed_list = []

i = len(l1) - 1
while i >= 0:
    reversed_list.append(l1[i])
    i = i - 1

print("Reversed list is - ", reversed_list)