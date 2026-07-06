"""Core ATM controller coordinating operations and session lifecycle."""
from __future__ import annotations
from typing import Optional
from atm_app.bank import Bank
from atm_app.models import Account, Transaction
from atm_app.storage import JSONStorageManager
from atm_app.security import verify_pin
from atm_app.exceptions import (
    AuthenticationError,
    AccountNotFoundError,
    AccountLockedError,
    ATMError,
)

class ATMController:
    def __init__(self, bank: Bank, storage: Optional[JSONStorageManager] = None):
        self.bank = bank
        self.storage = storage
        self.active_account: Optional[Account] = None

    def login(self, account_number: str, pin: str) -> Account:
        """Authenticate user by account number and PIN."""
        account = self.bank.get_account(account_number)
        if not account:
            raise AccountNotFoundError(f"Account '{account_number}' does not exist.")

        if account.is_locked:
            raise AccountLockedError(f"Account locked: {account.lock_reason}")

        if not verify_pin(pin, account.pin_hash, account.pin_salt):
            locked = account.record_failed_pin()
            if self.storage:
                self.storage.save(self.bank)
            if locked:
                raise AccountLockedError("Account locked due to 3 consecutive failed PIN attempts.")
            remaining = 3 - account.failed_pin_attempts
            raise AuthenticationError(f"Incorrect PIN. {remaining} attempt(s) remaining.")

        account.reset_failed_pin()
        self.active_account = account
        if self.storage:
            self.storage.save(self.bank)
        return account

    def logout(self) -> None:
        """Terminate currently active session."""
        self.active_account = None

    def get_balance(self) -> float:
        if not self.active_account:
            raise ATMError("No authenticated session.")
        return self.active_account.balance

    def deposit(self, amount: float) -> Transaction:
        if not self.active_account:
            raise ATMError("No authenticated session.")
        tx = self.active_account.deposit(amount)
        if self.storage:
            self.storage.save(self.bank)
        return tx

    def withdraw(self, amount: float) -> Transaction:
        if not self.active_account:
            raise ATMError("No authenticated session.")
        tx = self.active_account.withdraw(amount)
        if self.storage:
            self.storage.save(self.bank)
        return tx
