"""Main executable CLI driver for the ATM Banking Simulator."""
import sys
from atm_app.bank import Bank
from atm_app.config import Config
from atm_app.storage import JSONStorageManager
from atm_app.dispenser import CashDispenser
from atm_app.controller import ATMController
from atm_app.admin import AdminController
from atm_app.security import hash_pin
from atm_app.receipt import ReceiptGenerator
from atm_app.logger import setup_logger
from atm_app.ui import (
    print_banner,
    print_header,
    print_menu,
    print_success,
    print_error,
    print_transactions_table,
)
from atm_app.exceptions import ATMError

def customer_session(controller: ATMController, config: Config, logger):
    while True:
        acc = controller.active_account
        print(f"\nLogged in as: {acc.holder_name} (Acc: {acc.account_number})")
        options = [
            "Check Balance",
            "Withdraw Cash",
            "Deposit Cash",
            "Transfer Funds",
            "Mini Statement (Last 5)",
            "Full Statement",
            "Change Security PIN",
            "Log Out",
        ]
        print_menu(options)
        choice = input("\nEnter choice [1-8]: ").strip()

        if choice == "1":
            bal = controller.get_balance()
            print(f"\nAvailable Balance: {config.currency_symbol}{bal:,.2f}")

        elif choice == "2":
            try:
                amt = float(input(f"Enter withdrawal amount (Multiple of 100): "))
                tx = controller.withdraw(amt)
                logger.info(f"Withdrawal of {amt} successful on account {acc.account_number}")
                print_success(f"Please collect your cash: {config.currency_symbol}{amt:,.2f}")
                print(f"New Balance: {config.currency_symbol}{tx.balance_after:,.2f}")
                receipt_choice = input("Print receipt? (y/n): ").strip().lower()
                if receipt_choice == "y":
                    print("\n" + ReceiptGenerator.generate(config.bank_name, config.atm_id, acc, tx, config.currency_symbol))
            except (ATMError, ValueError) as e:
                print_error(str(e))

        elif choice == "3":
            try:
                amt = float(input("Enter deposit amount: "))
                tx = controller.deposit(amt)
                logger.info(f"Deposit of {amt} successful on account {acc.account_number}")
                print_success(f"Successfully deposited {config.currency_symbol}{amt:,.2f}")
                print(f"New Balance: {config.currency_symbol}{tx.balance_after:,.2f}")
            except (ATMError, ValueError) as e:
                print_error(str(e))

        elif choice == "4":
            try:
                target = input("Enter recipient account number: ").strip()
                amt = float(input("Enter transfer amount: "))
                out_tx, _ = controller.transfer_funds(target, amt)
                logger.info(f"Transfer of {amt} from {acc.account_number} to {target} completed.")
                print_success(f"Transfer of {config.currency_symbol}{amt:,.2f} completed successfully.")
            except (ATMError, ValueError) as e:
                print_error(str(e))

        elif choice == "5":
            txs = controller.get_mini_statement()
            print_header("Mini Statement")
            print_transactions_table(txs, config.currency_symbol)

        elif choice == "6":
            txs = controller.get_full_statement()
            print_header("Full Statement")
            print_transactions_table(txs, config.currency_symbol)

        elif choice == "7":
            try:
                old_p = input("Enter current PIN: ").strip()
                new_p = input("Enter new 4-digit PIN: ").strip()
                controller.change_pin(old_p, new_p)
                logger.info(f"PIN changed for account {acc.account_number}")
                print_success("PIN changed successfully.")
            except (ATMError, ValueError) as e:
                print_error(str(e))

        elif choice == "8":
            controller.logout()
            print("Logged out successfully.")
            break
        else:
            print_error("Invalid selection. Try again.")

def main():
    config = Config()
    logger = setup_logger()
    storage = JSONStorageManager()
    bank = storage.load(config.bank_name)
    dispenser = CashDispenser()
    controller = ATMController(bank, storage, dispenser)

    admin_hash, admin_salt = hash_pin(config.admin_pin)
    admin_controller = AdminController(bank, dispenser, admin_hash, admin_salt)

    while True:
        print_banner(config.bank_name, config.atm_id)
        menu = [
            "Cardholder Login",
            "Open New Account",
            "Administrator Portal",
            "Exit",
        ]
        print_menu(menu)
        ch = input("\nEnter option [1-4]: ").strip()

        if ch == "1":
            acc_num = input("Enter Account Number: ").strip()
            pin = input("Enter PIN: ").strip()
            try:
                controller.login(acc_num, pin)
                customer_session(controller, config, logger)
            except ATMError as e:
                logger.warning(f"Failed login attempt for account {acc_num}: {e}")
                print_error(str(e))

        elif ch == "2":
            name = input("Enter Account Holder Name: ").strip()
            pin = input("Set a 4-digit PIN: ").strip()
            try:
                deposit_amt = float(input("Enter initial deposit (min ₹500): "))
                new_acc = controller.register_account(name, pin, deposit_amt)
                print_success(f"Account created successfully!")
                print(f"Your Account Number is: {new_acc.account_number}")
            except (ATMError, ValueError) as e:
                print_error(str(e))

        elif ch == "3":
            adm_pin = input("Enter Administrator Passcode: ").strip()
            try:
                admin_controller.login(adm_pin)
                stats = admin_controller.get_system_audit()
                print_header("System Audit & Status")
                print(f"Total Accounts   : {stats['total_accounts']}")
                print(f"Total Deposits   : {config.currency_symbol}{stats['total_deposits']:,.2f}")
                print(f"ATM Cash Reserve : {config.currency_symbol}{stats['atm_cash_reserve']:,.2f}")
                print(f"Cassettes        : {stats['cassette_inventory']}")
                print(f"Locked Accounts  : {stats['locked_accounts']}")
                admin_controller.logout()
            except ATMError as e:
                print_error(str(e))

        elif ch == "4":
            print("\nThank you for using the ATM. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
