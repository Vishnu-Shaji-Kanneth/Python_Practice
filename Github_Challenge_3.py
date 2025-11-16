import random
user_choice = input("Enter your choice (stone/paper/scissor): ").lower()
options = ["stone", "paper", "scissor"]
computer_choice = random.choice(options)

print("You chose:", user_choice)
print("Computer chose:", computer_choice)

if user_choice == computer_choice:
    print("Result: It's a draw.")

elif user_choice == "stone":
    if computer_choice == "scissor":
        print("Result: You win.")
    else:
        print("Result: You lose.")

elif user_choice == "paper":
    if computer_choice == "stone":
        print("Result: You win.")
    else:
        print("Result: You lose.")

elif user_choice == "scissor":
    if computer_choice == "paper":
        print("Result: You win.")
    else:
        print("Result: You lose.")

else:
    print("Invalid input.")