class ATM:
    def __init__(self, balance=10000, pin=1234):
        self.balance = balance
        self.pin = pin
        self.transactions = []
        self.max_attempts = 3

    def authenticate(self):
        """Verify the user's PIN. Card is blocked after 3 failed attempts."""
        attempts = 0

        while attempts < self.max_attempts:
            try:
                user_pin = int(input("Enter the PIN: "))
            except ValueError:
                attempts += 1
                print("PIN must contain numbers only.")
                continue

            if user_pin == self.pin:
                print("Login successful!")
                return True

            attempts += 1
            remaining = self.max_attempts - attempts
            print("Wrong PIN.")

            if remaining > 0:
                print(f"Attempts remaining: {remaining}")

        print("Card blocked.")
        return False

    def check_balance(self):
        print(f"Available balance: ₹{self.balance}")

    def deposit(self):
        try:
            amount = int(input("Enter the amount to deposit: ₹"))
        except ValueError:
            print("Please enter a valid amount.")
            return

        if amount <= 0:
            print("Deposit amount must be greater than 0.")
            return

        self.balance += amount
        self.transactions.append(f"Deposited ₹{amount}")
        print(f"Deposit successful. Updated balance: ₹{self.balance}")

    def withdraw(self):
        try:
            amount = int(input("Enter the amount to withdraw: ₹"))
        except ValueError:
            print("Please enter a valid amount.")
            return

        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
        elif amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrawn ₹{amount}")
            print(f"Transaction successful. Remaining balance: ₹{self.balance}")

    def mini_statement(self):
        print("\n------------- Mini Statement -------------")

        if not self.transactions:
            print("No transactions found.")
            return

        for number, transaction in enumerate(self.transactions, start=1):
            print(f"{number}. {transaction}")

        print(f"Current balance: ₹{self.balance}")

    def change_pin(self):
        try:
            current_pin = int(input("Enter current PIN: "))
        except ValueError:
            print("PIN must contain numbers only.")
            return

        if current_pin != self.pin:
            print("Wrong PIN.")
            return

        try:
            new_pin = int(input("Enter the new 4-digit PIN: "))
        except ValueError:
            print("PIN must contain numbers only.")
            return

        if not 1000 <= new_pin <= 9999:
            print("PIN must be exactly 4 digits.")
        elif new_pin == self.pin:
            print("New PIN cannot be the same as the current PIN.")
        else:
            self.pin = new_pin
            print("PIN changed successfully.")

    def show_menu(self):
        print(
            "\nChoose an option:"
            "\n1. Check Balance"
            "\n2. Deposit"
            "\n3. Withdraw"
            "\n4. Mini Statement"
            "\n5. Change PIN"
            "\n6. Exit"
        )

    def run(self):
        print("Welcome to the ATM")

        if not self.authenticate():
            return

        while True:
            self.show_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.check_balance()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.mini_statement()
            elif choice == "5":
                self.change_pin()
            elif choice == "6":
                print("Thank you for using the ATM.")
                break
            else:
                print("Invalid option. Please choose from 1 to 6.")


if __name__ == "__main__":
    atm = ATM()
    atm.run()
