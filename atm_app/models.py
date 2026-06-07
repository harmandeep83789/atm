"""Domain models for ATM transactions and bank accounts."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from atm_app.exceptions import InsufficientFundsError, InvalidAmountError

class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"
    PIN_CHANGE = "PIN_CHANGE"

@dataclass
class Transaction:
    amount: float
    transaction_type: TransactionType
    balance_after: float
    description: str = ""
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8].upper())
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    reference_account: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "transaction_type": self.transaction_type.value,
            "amount": self.amount,
            "balance_after": self.balance_after,
            "description": self.description,
            "reference_account": self.reference_account,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Transaction:
        return cls(
            transaction_id=data["transaction_id"],
            timestamp=data["timestamp"],
            transaction_type=TransactionType(data["transaction_type"]),
            amount=float(data["amount"]),
            balance_after=float(data["balance_after"]),
            description=data.get("description", ""),
            reference_account=data.get("reference_account"),
        )

@dataclass
class Account:
    account_number: str
    holder_name: str
    pin_hash: str
    pin_salt: str
    balance: float = 0.0
    transactions: List[Transaction] = field(default_factory=list)
    failed_pin_attempts: int = 0
    is_locked: bool = False
    lock_reason: Optional[str] = None

    def deposit(self, amount: float, description: str = "Deposit") -> Transaction:
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be strictly positive.")
        self.balance += amount
        tx = Transaction(
            amount=amount,
            transaction_type=TransactionType.DEPOSIT,
            balance_after=self.balance,
            description=description,
        )
        self.transactions.append(tx)
        return tx

    def withdraw(self, amount: float, description: str = "Withdrawal") -> Transaction:
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be strictly positive.")
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Balance: {self.balance}, Requested: {amount}")
        self.balance -= amount
        tx = Transaction(
            amount=amount,
            transaction_type=TransactionType.WITHDRAWAL,
            balance_after=self.balance,
            description=description,
        )
        self.transactions.append(tx)
        return tx

    def record_failed_pin(self, max_attempts: int = 3) -> bool:
        """Increments failed attempt counter. Locks account if threshold reached."""
        self.failed_pin_attempts += 1
        if self.failed_pin_attempts >= max_attempts:
            self.is_locked = True
            self.lock_reason = f"Exceeded maximum failed PIN attempts ({max_attempts})"
            return True
        return False

    def reset_failed_pin(self) -> None:
        """Reset failed attempt counter after successful authentication."""
        self.failed_pin_attempts = 0

    def unlock(self) -> None:
        """Administratively unlock account and reset counter."""
        self.is_locked = False
        self.failed_pin_attempts = 0
        self.lock_reason = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "pin_hash": self.pin_hash,
            "pin_salt": self.pin_salt,
            "balance": self.balance,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "failed_pin_attempts": self.failed_pin_attempts,
            "is_locked": self.is_locked,
            "lock_reason": self.lock_reason,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Account:
        txs = [Transaction.from_dict(t) for t in data.get("transactions", [])]
        return cls(
            account_number=data["account_number"],
            holder_name=data["holder_name"],
            pin_hash=data["pin_hash"],
            pin_salt=data["pin_salt"],
            balance=float(data["balance"]),
            transactions=txs,
            failed_pin_attempts=data.get("failed_pin_attempts", 0),
            is_locked=data.get("is_locked", False),
            lock_reason=data.get("lock_reason"),
        )
