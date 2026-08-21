"""Administrator portal controller for ATM management."""
from typing import Dict, Any
from atm_app.bank import Bank
from atm_app.dispenser import CashDispenser
from atm_app.security import verify_pin, hash_pin
from atm_app.exceptions import AuthenticationError

class AdminController:
    def __init__(self, bank: Bank, dispenser: CashDispenser, admin_pin_hash: str, admin_pin_salt: str):
        self.bank = bank
        self.dispenser = dispenser
        self.admin_pin_hash = admin_pin_hash
        self.admin_pin_salt = admin_pin_salt
        self.is_authenticated = False

    def login(self, pin: str) -> bool:
        if verify_pin(pin, self.admin_pin_hash, self.admin_pin_salt):
            self.is_authenticated = True
            return True
        raise AuthenticationError("Invalid Admin Passcode.")

    def logout(self) -> None:
        self.is_authenticated = False

    def get_system_audit(self) -> Dict[str, Any]:
        if not self.is_authenticated:
            raise AuthenticationError("Admin session required.")
        accounts = self.bank.list_accounts()
        total_txs = sum(len(a.transactions) for a in accounts)
        locked_accounts = [a.account_number for a in accounts if a.is_locked]
        return {
            "total_accounts": len(accounts),
            "total_deposits": self.bank.total_deposits,
            "atm_cash_reserve": self.dispenser.total_cash_available,
            "cassette_inventory": dict(self.dispenser.cassettes),
            "total_transactions": total_txs,
            "locked_accounts": locked_accounts,
        }

    def unlock_account(self, account_number: str) -> None:
        if not self.is_authenticated:
            raise AuthenticationError("Admin session required.")
        acc = self.bank.get_account(account_number)
        if acc:
            acc.unlock()

    def refill_atm(self, notes: Dict[int, int]) -> None:
        if not self.is_authenticated:
            raise AuthenticationError("Admin session required.")
        self.dispenser.refill(notes)
