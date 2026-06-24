"""Persistence manager with atomic writes and backup recovery."""
from __future__ import annotations
import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any
from atm_app.bank import Bank
from atm_app.models import Account

class JSONStorageManager:
    def __init__(self, data_dir: str | Path = "data"):
        self.data_dir = Path(data_dir)
        self.data_file = self.data_dir / "bank_data.json"
        self.backup_file = self.data_dir / "bank_data.json.bak"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, bank: Bank) -> None:
        """Safely saves bank data atomically via a temporary file."""
        data: Dict[str, Any] = {
            "bank_name": bank.name,
            "accounts": [acc.to_dict() for acc in bank.list_accounts()],
        }
        # Backup existing file before overwrite
        if self.data_file.exists():
            try:
                shutil.copyfile(self.data_file, self.backup_file)
            except OSError:
                pass

        temp_file = self.data_dir / f"bank_data_{os.getpid()}.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_file, self.data_file)

    def load(self, bank_name: str = "Apex Trust Bank") -> Bank:
        """Loads bank data with fallback to backup file if corruption occurs."""
        bank = Bank(name=bank_name)
        target = self.data_file if self.data_file.exists() else self.backup_file
        if not target.exists():
            return bank

        try:
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
            bank.name = data.get("bank_name", bank_name)
            for acc_data in data.get("accounts", []):
                bank.add_account(Account.from_dict(acc_data))
        except (json.JSONDecodeError, KeyError):
            if target != self.backup_file and self.backup_file.exists():
                with open(self.backup_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                bank.name = data.get("bank_name", bank_name)
                for acc_data in data.get("accounts", []):
                    bank.add_account(Account.from_dict(acc_data))
        return bank
