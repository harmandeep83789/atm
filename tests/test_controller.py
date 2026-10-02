import unittest
from atm_app.bank import Bank
from atm_app.models import Account
from atm_app.controller import ATMController
from atm_app.security import hash_pin
from atm_app.exceptions import (
    AuthenticationError,
    AccountLockedError,
    InsufficientFundsError,
    DailyLimitExceededError,
)

class TestATMController(unittest.TestCase):
    def setUp(self):
        self.bank = Bank("Test Bank")
        h, s = hash_pin("1234")
        self.acc1 = Account("1001", "User One", h, s, 5000.0)
        h2, s2 = hash_pin("5678")
        self.acc2 = Account("1002", "User Two", h2, s2, 2000.0)
        self.bank.add_account(self.acc1)
        self.bank.add_account(self.acc2)
        self.controller = ATMController(self.bank)

    def test_successful_login(self):
        acc = self.controller.login("1001", "1234")
        self.assertEqual(acc.account_number, "1001")
        self.assertEqual(self.controller.get_balance(), 5000.0)

    def test_lockout_after_three_attempts(self):
        with self.assertRaises(AuthenticationError):
            self.controller.login("1001", "9999")
        with self.assertRaises(AuthenticationError):
            self.controller.login("1001", "9999")
        with self.assertRaises(AccountLockedError):
            self.controller.login("1001", "9999")
        self.assertTrue(self.acc1.is_locked)

    def test_transfer_funds(self):
        self.controller.login("1001", "1234")
        self.controller.transfer_funds("1002", 1500.0)
        self.assertEqual(self.acc1.balance, 3500.0)
        self.assertEqual(self.acc2.balance, 3500.0)

    def test_daily_limit(self):
        self.controller.login("1001", "1234")
        self.acc1.balance = 50000.0
        self.controller.withdraw(10000.0)
        self.controller.withdraw(10000.0)
        with self.assertRaises(DailyLimitExceededError):
            self.controller.withdraw(10000.0)
