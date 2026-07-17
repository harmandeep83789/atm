"""Core ATM controller coordinating operations, transfers, PIN changes, and sessions."""
from __future__ import annotations
from typing import Optional, Tuple
from atm_app.bank import Bank
from atm_app.models import Account, Transaction, TransactionType
from atm_app.storage import JSONStorageManager
from atm_app.security import verify_pin, hash_pin, validate_pin_format
from atm_app.exceptions import (
    AuthenticationError,
    AccountNotFoundError,
    AccountLockedError,
    ATMError,
    InvalidAmountError,
    InsufficientFundsError,
)

class ATMController:
    def __init__(self, bank: Bank, storage: Optional[JSONStorageManager] = None):
        self.bank = bank
        self.storage = storage
        self.active_account: Optional[Account] = None

    def login(self, account_number: str, pin: str) -> Account:
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

    def transfer_funds(self, target_account_number: str, amount: float) -> Tuple[Transaction, Transaction]:
        if not self.active_account:
            raise ATMError("No authenticated session.")
        if amount <= 0:
            raise InvalidAmountError("Transfer amount must be positive.")
        if target_account_number == self.active_account.account_number:
            raise InvalidAmountError("Cannot transfer funds to the same account.")

        target = self.bank.get_account(target_account_number)
        if not target:
            raise AccountNotFoundError(f"Recipient account '{target_account_number}' not found.")
        if target.is_locked:
            raise AccountLockedError(f"Recipient account '{target_account_number}' is frozen.")
        if amount > self.active_account.balance:
            raise InsufficientFundsError(
                f"Insufficient balance ({self.active_account.balance}) to transfer {amount}."
            )

        self.active_account.balance -= amount
        out_tx = Transaction(
            amount=amount,
            transaction_type=TransactionType.TRANSFER_OUT,
            balance_after=self.active_account.balance,
            description=f"Transfer to {target.holder_name} ({target_account_number})",
            reference_account=target_account_number,
        )
        self.active_account.transactions.append(out_tx)

        target.balance += amount
        in_tx = Transaction(
            amount=amount,
            transaction_type=TransactionType.TRANSFER_IN,
            balance_after=target.balance,
            description=f"Transfer from {self.active_account.holder_name} ({self.active_account.account_number})",
            reference_account=self.active_account.account_number,
        )
        target.transactions.append(in_tx)

        if self.storage:
            self.storage.save(self.bank)
        return out_tx, in_tx

    def change_pin(self, old_pin: str, new_pin: str) -> None:
        """Securely changes account PIN after confirming old PIN."""
        if not self.active_account:
            raise ATMError("No authenticated session.")
        if not verify_pin(old_pin, self.active_account.pin_hash, self.active_account.pin_salt):
            raise AuthenticationError("Current PIN is incorrect.")
        if not validate_pin_format(new_pin):
            raise AuthenticationError("New PIN must be 4 to 6 numeric digits.")
        if old_pin == new_pin:
            raise AuthenticationError("New PIN cannot be identical to current PIN.")

        new_hash, new_salt = hash_pin(new_pin)
        self.active_account.pin_hash = new_hash
        self.active_account.pin_salt = new_salt
        tx = Transaction(
            amount=0.0,
            transaction_type=TransactionType.PIN_CHANGE,
            balance_after=self.active_account.balance,
            description="Security PIN updated successfully",
        )
        self.active_account.transactions.append(tx)
        if self.storage:
            self.storage.save(self.bank)
