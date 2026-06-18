"""Persistence manager for storing accounts and transactions to JSON."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any
from atm_app.bank import Bank
from atm_app.models import Account

class JSONStorageManager:
    def __init__(self, data_dir: str | Path = "data"):
        self.data_dir = Path(data_dir)
        self.data_file = self.data_dir / "bank_data.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, bank: Bank) -> None:
        data: Dict[str, Any] = {
            "bank_name": bank.name,
            "accounts": [acc.to_dict() for acc in bank.list_accounts()],
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, bank_name: str = "Apex Trust Bank") -> Bank:
        bank = Bank(name=bank_name)
        if not self.data_file.exists():
            return bank

        with open(self.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        bank.name = data.get("bank_name", bank_name)
        for acc_data in data.get("accounts", []):
            acc = Account.from_dict(acc_data)
            bank.add_account(acc)
        return bank
