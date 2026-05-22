"""Domain models for ATM transactions and bank accounts."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

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
