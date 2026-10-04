import unittest
import tempfile
import shutil
from pathlib import Path
from atm_app.bank import Bank
from atm_app.models import Account
from atm_app.storage import JSONStorageManager

class TestStorageManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage = JSONStorageManager(data_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_save_and_load(self):
        bank = Bank("Apex Bank")
        acc = Account("9999", "Tester", "h", "s", 1234.0)
        bank.add_account(acc)
        self.storage.save(bank)

        loaded_bank = self.storage.load()
        self.assertTrue(loaded_bank.account_exists("9999"))
        self.assertEqual(loaded_bank.get_account("9999").balance, 1234.0)
