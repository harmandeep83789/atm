balance = 1000
transactions = []

def show_balance():
    print("Balance:", balance)

def deposit():
    global balance
    amt = int(input("Enter amount: "))
    balance += amt
    transactions.append("Deposit: " + str(amt))
    print("Deposited")

def withdraw():
    global balance
    amt = int(input("Enter amount: "))
    if amt <= balance:
        balance -= amt
        transactions.append("Withdraw: " + str(amt))
        print("Withdrawn")
    else:
        print("Not enough balance")

def statement():
    if len(transactions) == 0:
        print("No transactions")
    else:
        for t in transactions:
            print(t)