balance = 1000
transactions = []

def get_valid_amount(prompt: str) -> int:
    while True:
        try:
            val = int(input(prompt))
            if val <= 0:
                print("Amount must be greater than zero.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def show_balance():
    print(f"Balance: ₹{balance:,.2f}")

def deposit():
    global balance
    amt = get_valid_amount("Enter amount to deposit: ")
    balance += amt
    transactions.append(f"Deposit: +₹{amt:,.2f}")
    print("Deposited successfully.")

def withdraw():
    global balance
    amt = get_valid_amount("Enter amount to withdraw: ")
    if amt <= balance:
        balance -= amt
        transactions.append(f"Withdraw: -₹{amt:,.2f}")
        print("Withdrawn successfully.")
    else:
        print("Error: Insufficient balance.")

def statement():
    if not transactions:
        print("No transactions on record.")
    else:
        print("--- Transaction Statement ---")
        for t in transactions:
            print(t)
