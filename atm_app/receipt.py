"""Receipt formatting and generation engine."""
from datetime import datetime
from typing import Optional
from atm_app.models import Account, Transaction

class ReceiptGenerator:
    @staticmethod
    def mask_account(acc_num: str) -> str:
        if len(acc_num) <= 4:
            return acc_num
        return "*" * (len(acc_num) - 4) + acc_num[-4:]

    @classmethod
    def generate(
        cls,
        bank_name: str,
        atm_id: str,
        account: Account,
        tx: Transaction,
        currency_sym: str = "₹"
    ) -> str:
        lines = [
            "=========================================",
            f"          {bank_name.center(25)}",
            f"          ATM ID: {atm_id.center(21)}",
            "=========================================",
            f" Date/Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f" Tx ID     : {tx.transaction_id}",
            f" Account   : {cls.mask_account(account.account_number)}",
            f" Holder    : {account.holder_name}",
            "-----------------------------------------",
            f" Tx Type   : {tx.transaction_type.value}",
            f" Amount    : {currency_sym}{tx.amount:,.2f}",
            f" Available : {currency_sym}{tx.balance_after:,.2f}",
            "-----------------------------------------",
            "      Thank you for banking with us!     ",
            "        Please retain your receipt.      ",
            "=========================================",
        ]
        return "\n".join(lines)
