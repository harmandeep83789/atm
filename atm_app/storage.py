"""Persistence manager with atomic writes, backup recovery, and seed accounts."""
from __future__ import annotations
import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any
from atm_app.bank import Bank
from atm_app.models import Account
from atm_app.security import hash_pin

class JSONStorageManager:
    def __init__(self, data_dir: str | Path = "data"):
        self.data_dir = Path(data_dir)
        self.data_file = self.data_dir / "bank_data.json"
        self.backup_file = self.data_dir / "bank_data.json.bak"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def seed_defaults(self, bank: Bank) -> None:
        """Seed initial demo accounts if bank is completely empty."""
        seeds = [
            ("1001", "Harmandeep Singh", "1234", 15000.0),
            ("1002", "Alex Mercer", "4321", 8500.0),
            ("1003", "Elena Rostova", "9876", 24000.0),
        ]
        for acc_num, name, pin, initial_bal in seeds:
            if not bank.account_exists(acc_num):
                p_hash, p_salt = hash_pin(pin)
                acc = Account(
                    account_number=acc_num,
                    holder_name=name,
                    pin_hash=p_hash,
                    pin_salt=p_salt,
                )
                acc.deposit(initial_bal, description="Initial Deposit (Account Opening)")
                bank.add_account(acc)
        self.save(bank)

    def save(self, bank: Bank) -> None:
        data: Dict[str, Any] = {
            "bank_name": bank.name,
            "accounts": [acc.to_dict() for acc in bank.list_accounts()],
        }
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
        bank = Bank(name=bank_name)
        target = self.data_file if self.data_file.exists() else self.backup_file
        if not target.exists():
            self.seed_defaults(bank)
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
        if bank.total_accounts_count == 0:
            self.seed_defaults(bank)
        return bank
