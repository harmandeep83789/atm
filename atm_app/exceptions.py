"""Custom banking and ATM domain exceptions."""

class ATMError(Exception):
    """Base exception for all ATM application errors."""
    pass

class AuthenticationError(ATMError):
    """Raised when authentication credentials fail."""
    pass

class AccountLockedError(AuthenticationError):
    """Raised when an account is locked due to security limits."""
    pass

class AccountNotFoundError(ATMError):
    """Raised when an account cannot be located."""
    pass

class AccountAlreadyExistsError(ATMError):
    """Raised when attempting to create a duplicate account."""
    pass

class InsufficientFundsError(ATMError):
    """Raised when an account has insufficient balance for an operation."""
    pass

class InvalidAmountError(ATMError):
    """Raised when a monetary amount is negative, zero, or non-viable."""
    pass

class DailyLimitExceededError(ATMError):
    """Raised when a withdrawal exceeds daily allowance."""
    pass

class CashDispenserError(ATMError):
    """Raised when the ATM cash dispenser cannot fulfill a withdrawal."""
    pass
