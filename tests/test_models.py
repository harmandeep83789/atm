import unittest
from atm_app.models import Account, Transaction, TransactionType
from atm_app.exceptions import InsufficientFundsError, InvalidAmountError

class TestAccountAndTransactions(unittest.TestCase):
    def setUp(self):
        self.account = Account(
            account_number="1234",
            holder_name="Test Holder",
            pin_hash="hash",
            pin_salt="salt",
            balance=1000.0,
        )

    def test_deposit_valid(self):
        tx = self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(tx.amount, 500.0)
        self.assertEqual(tx.transaction_type, TransactionType.DEPOSIT)

    def test_deposit_invalid(self):
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(-50.0)

    def test_withdraw_valid(self):
        tx = self.account.withdraw(400.0)
        self.assertEqual(self.account.balance, 600.0)
        self.assertEqual(tx.amount, 400.0)
        self.assertEqual(tx.transaction_type, TransactionType.WITHDRAWAL)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(2000.0)

    def test_serialization(self):
        d = self.account.to_dict()
        restored = Account.from_dict(d)
        self.assertEqual(restored.account_number, self.account.account_number)
        self.assertEqual(restored.balance, self.account.balance)
