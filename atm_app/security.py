"""Security utilities for cryptographic PIN hashing and verification."""
import hashlib
import os
import re
from typing import Tuple

def generate_salt(length: int = 16) -> str:
    """Generate a cryptographically secure random hexadecimal salt."""
    return os.urandom(length).hex()

def hash_pin(pin: str, salt: str | None = None) -> Tuple[str, str]:
    """
    Hash a numeric PIN using SHA-256 and a random cryptographic salt.
    Returns (hashed_value, salt).
    """
    if salt is None:
        salt = generate_salt()
    combined = (salt + pin).encode("utf-8")
    pin_hash = hashlib.sha256(combined).hexdigest()
    return pin_hash, salt

def verify_pin(pin: str, stored_hash: str, salt: str) -> bool:
    """Verify an entered PIN against stored hash and salt."""
    computed_hash, _ = hash_pin(pin, salt)
    return computed_hash == stored_hash

def validate_pin_format(pin: str) -> bool:
    """Validate that PIN is exactly 4 to 6 numeric digits."""
    return bool(re.fullmatch(r"\d{4,6}", pin))
