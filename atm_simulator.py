class ATM:
    def __init__(self, account_holder, pin, balance=0):
        self.account_holder = account_holder
        self.pin = pin
        self.balance = balance

    def check_balance(self, entered_pin):
        if entered_pin == self.pin:
            print(f"Current balance: ₹{self.balance}")
        else:
            print("Incorrect PIN")

    def deposit(self, amount, entered_pin):
        if entered_pin == self.pin:
            if amount > 0:
                self.balance += amount
                print(f"₹{amount} deposited successfully")
            else:
                print("Invalid deposit amount")
        else:
            print("Incorrect PIN")

    def withdraw(self, amount, entered_pin):
        if entered_pin == self.pin:
            if amount <= 0:
                print("Invalid withdrawal amount")
            elif amount > self.balance:
                print("Insufficient balance")
            else:
                self.balance -= amount
                print(f"₹{amount} withdrawn successfully")
        else:
            print("Incorrect PIN")

    def change_pin(self, old_pin, new_pin):
        if old_pin == self.pin:
            if len(str(new_pin)) == 4:
                self.pin = new_pin
                print("PIN changed successfully")
            else:
                print("New PIN must be 4 digits")
        else:
            print("Incorrect old PIN")


# -------------------- TESTING --------------------
if __name__ == "__main__":
    atm = ATM("Vishnu", 1234)

    atm.check_balance(1234)
    atm.deposit(5000, 1234)
    atm.withdraw(2000, 1234)
    atm.check_balance(1234)
    atm.change_pin(1234, 2156)
    atm.check_balance(2156)
