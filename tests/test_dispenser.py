import unittest
from atm_app.dispenser import CashDispenser
from atm_app.exceptions import CashDispenserError

class TestCashDispenser(unittest.TestCase):
    def setUp(self):
        self.dispenser = CashDispenser({2000: 2, 500: 4, 100: 10})

    def test_dispense_calculation(self):
        plan = self.dispenser.dispense(2500)
        self.assertEqual(plan.get(2000), 1)
        self.assertEqual(plan.get(500), 1)
        self.assertEqual(self.dispenser.total_cash_available, 4500)

    def test_invalid_denomination(self):
        with self.assertRaises(CashDispenserError):
            self.dispenser.dispense(150)
