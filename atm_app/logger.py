"""Audit logging configuration for ATM security and operations."""
import logging
from pathlib import Path

def setup_logger(log_file: str | Path = "atm.log") -> logging.Logger:
    logger = logging.getLogger("ATMApp")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [ATM-AUDIT] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
