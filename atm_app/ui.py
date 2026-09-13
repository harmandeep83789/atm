"""Terminal User Interface components and formatting utilities."""
import os
from typing import List
from atm_app.models import Transaction

def clear_screen() -> None:
    # Safe terminal clear
    os.system("clear" if os.name != "nt" else "cls")

def print_banner(bank_name: str, atm_id: str) -> None:
    print("=" * 50)
    print(f" {bank_name.upper()} ".center(50, "*"))
    print(f" Terminal: {atm_id} ".center(50))
    print("=" * 50)

def print_header(title: str) -> None:
    print(f"\n--- {title} ---")

def print_success(msg: str) -> None:
    print(f"\033[92m✔ {msg}\033[0m")

def print_error(msg: str) -> None:
    print(f"\033[91m✖ Error: {msg}\033[0m")

def print_menu(options: List[str]) -> None:
    print("\nSelect an operation:")
    for idx, opt in enumerate(options, 1):
        print(f" [{idx}] {opt}")

def print_transactions_table(transactions: List[Transaction], currency_sym: str = "₹") -> None:
    if not transactions:
        print("No transactions to display.")
        return
    print("-" * 75)
    print(f"{'TX ID':<10} | {'DATE/TIME':<19} | {'TYPE':<12} | {'AMOUNT':<12} | {'BALANCE':<12}")
    print("-" * 75)
    for tx in transactions:
        t_time = tx.timestamp[:19].replace("T", " ")
        sign = "+" if "DEPOSIT" in tx.transaction_type.value or "IN" in tx.transaction_type.value else "-"
        amt_str = f"{sign}{currency_sym}{tx.amount:,.2f}"
        bal_str = f"{currency_sym}{tx.balance_after:,.2f}"
        print(f"{tx.transaction_id:<10} | {t_time:<19} | {tx.transaction_type.value:<12} | {amt_str:<12} | {bal_str:<12}")
    print("-" * 75)
