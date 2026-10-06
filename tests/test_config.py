import unittest
import tempfile
from pathlib import Path
from atm_app.config import Config

class TestConfig(unittest.TestCase):
    def test_default_config(self):
        cfg = Config()
        self.assertEqual(cfg.bank_name, "Apex Trust Bank")
        self.assertEqual(cfg.currency_symbol, "₹")
        self.assertEqual(cfg.min_withdrawal, 100.0)

    def test_save_and_load(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            cfg = Config(bank_name="Custom Bank", min_withdrawal=200.0)
            cfg.save(tmp_path)
            loaded = Config.load(tmp_path)
            self.assertEqual(loaded.bank_name, "Custom Bank")
            self.assertEqual(loaded.min_withdrawal, 200.0)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
