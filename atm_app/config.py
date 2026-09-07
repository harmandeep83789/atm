"""Configuration management with customizable limits and settings."""
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class Config:
    bank_name: str = "Apex Trust Bank"
    atm_id: str = "ATM-APEX-042"
    currency_symbol: str = "₹"
    daily_withdrawal_limit: float = 25000.0
    max_single_withdrawal: float = 10000.0
    min_withdrawal: float = 100.0
    admin_pin: str = "9999"

    @classmethod
    def load(cls, config_path: str | Path = "config.json") -> "Config":
        path = Path(config_path)
        if not path.exists():
            return cls()
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(**data)
        except Exception:
            return cls()

    def save(self, config_path: str | Path = "config.json") -> None:
        path = Path(config_path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, indent=2)
