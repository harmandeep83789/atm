"""Bank repository for managing multi-user customer accounts."""
from __future__ import annotations
from typing import Dict, List, Optional
from atm_app.models import Account
from atm_app.exceptions import AccountAlreadyExistsError

class Bank:
    def __init__(self, name: str = "Apex Trust Bank"):
        self.name = name
        self._accounts: Dict[str, Account] = {}

    def add_account(self, account: Account) -> None:
        if account.account_number in self._accounts:
            raise AccountAlreadyExistsError(f"Account {account.account_number} already exists.")
        self._accounts[account.account_number] = account

    def get_account(self, account_number: str) -> Optional[Account]:
        return self._accounts.get(account_number)

    def account_exists(self, account_number: str) -> bool:
        return account_number in self._accounts

    def list_accounts(self) -> List[Account]:
        return list(self._accounts.values())

    @property
    def total_deposits(self) -> float:
        return sum(acc.balance for acc in self._accounts.values())

    @property
    def total_accounts_count(self) -> int:
        return len(self._accounts)
