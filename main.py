import atm

choice = 0

while choice != 5:
    print("\n1. Balance")
    print("2. Withdraw")
    print("3. Deposit")
    print("4. Statement")
    print("5. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        atm.show_balance()
    elif choice == 2:
        atm.withdraw()
    elif choice == 3:
        atm.deposit()
    elif choice == 4:
        atm.statement()
    elif choice == 5:
        print("Exit")
    else:
        print("Invalid choice")