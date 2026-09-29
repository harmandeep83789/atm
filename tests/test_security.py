import unittest
from atm_app.security import hash_pin, verify_pin, validate_pin_format

class TestSecurity(unittest.TestCase):
    def test_hash_and_verify(self):
        pin = "4321"
        p_hash, p_salt = hash_pin(pin)
        self.assertTrue(verify_pin(pin, p_hash, p_salt))
        self.assertFalse(verify_pin("0000", p_hash, p_salt))

    def test_validate_pin_format(self):
        self.assertTrue(validate_pin_format("1234"))
        self.assertTrue(validate_pin_format("123456"))
        self.assertFalse(validate_pin_format("123"))
        self.assertFalse(validate_pin_format("abcd"))
        self.assertFalse(validate_pin_format("1234567"))
