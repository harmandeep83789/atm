"""Backwards-compatible legacy facade delegating to the modular atm_app package."""
import warnings
from atm_app.bank import Bank
from atm_app.config import Config
from atm_app.storage import JSONStorageManager
from atm_app.dispenser import CashDispenser
from atm_app.controller import ATMController
from atm_app.ui import print_transactions_table

warnings.warn(
    "Importing from atm.py is deprecated. Use the atm_app package and main.py instead.",
    DeprecationWarning,
    stacklevel=2,
)

_config = Config()
_storage = JSONStorageManager()
_bank = _storage.load(_config.bank_name)
_dispenser = CashDispenser()
_controller = ATMController(_bank, _storage, _dispenser)

# Default to seed account 1001 for legacy script callers
_account = _bank.get_account("1001")
if _account:
    _controller.active_account = _account

def show_balance():
    if _controller.active_account:
        print(f"Balance: ₹{_controller.active_account.balance:,.2f}")
    else:
        print("No active account.")

def deposit():
    if not _controller.active_account:
        print("No active account.")
        return
    try:
        amt = float(input("Enter amount: "))
        _controller.deposit(amt)
        print("Deposited successfully.")
    except Exception as e:
        print(f"Error: {e}")

def withdraw():
    if not _controller.active_account:
        print("No active account.")
        return
    try:
        amt = float(input("Enter amount: "))
        _controller.withdraw(amt)
        print("Withdrawn successfully.")
    except Exception as e:
        print(f"Error: {e}")

def statement():
    if not _controller.active_account:
        print("No active account.")
        return
    txs = _controller.get_full_statement()
    if not txs:
        print("No transactions")
    else:
        print_transactions_table(txs)
