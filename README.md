# ATM Simulator System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: 16 Passing](https://img.shields.io/badge/tests-16%20passing-brightgreen.svg)](run_tests.py)

A modular, robust, and secure Automated Teller Machine (ATM) banking simulation system written in modern Python.

---

## 🌟 Key Features

- **🔐 Cryptographic Security**: Salted SHA-256 PIN hashing with automated account lockouts after 3 consecutive failed attempts.
- **🏦 Multi-Account Architecture**: Full bank repository supporting independent user accounts, balances, and transaction ledgers.
- **💸 Comprehensive Operations**:
  - Cash Deposit and Withdrawal
  - Inter-Account Fund Transfers with double-entry ledger tracking
  - Change Security PIN with old PIN verification
  - Mini-Statements (recent 5) and Full Transaction Ledgers
  - Search and filter transactions by type and amount
- **💵 Physical Cash Cassettes**: Simulated ATM dispenser tracking banknotes of ₹2000, ₹500, ₹200, and ₹100 using a greedy dispensing algorithm.
- **💾 Atomic Persistence**: Safe JSON storage with temporary file writes and automatic `.bak` recovery.
- **🛡️ Administrator Portal**: Dedicated admin tools to refill cash, inspect total deposits, and unlock frozen accounts.
- **🧾 Printable Receipts**: ASCII formatted printable transaction receipts.
- **🧪 100% Test Coverage**: Complete test suite using Python `unittest` test discovery.

---

## 📂 Project Structure

```
atm/
├── atm_app/                # Core banking application package
│   ├── __init__.py         # Package metadata
│   ├── admin.py            # Administrator controller & audit
│   ├── bank.py             # Bank repository managing customer accounts
│   ├── config.py           # Configuration management
│   ├── controller.py       # Main ATM controller & transaction policies
│   ├── dispenser.py        # Banknote cassette & dispensing engine
│   ├── exceptions.py       # Domain exception hierarchy
│   ├── logger.py           # Structured security audit logger
│   ├── models.py           # Account and Transaction dataclasses
│   ├── receipt.py          # Printable ASCII receipt generator
│   ├── security.py         # Salted SHA-256 hashing & validation
│   ├── storage.py          # Atomic JSON persistence & seed generator
│   └── ui.py               # Rich terminal UI components
├── tests/                  # Automated unit test suite
│   ├── test_config.py
│   ├── test_controller.py
│   ├── test_dispenser.py
│   ├── test_models.py
│   ├── test_security.py
│   └── test_storage.py
├── main.py                 # Primary CLI application entry point
├── atm.py                  # Backwards-compatible legacy module
├── run_tests.py            # Test discovery runner
├── pyproject.toml          # Packaging metadata
├── requirements.txt        # Development dependencies
└── README.md               # Documentation
```

---

## 🚀 Quick Start

### 1. Run the ATM Simulator
```bash
python3 main.py
```

### 2. Demo Seed Accounts
On first run, default demo accounts are automatically prepared:
| Account Number | Holder Name | Default PIN | Initial Balance |
| :--- | :--- | :--- | :--- |
| **1001** | Harmandeep Singh | `1234` | ₹15,000.00 |
| **1002** | Alex Mercer | `4321` | ₹8,500.00 |
| **1003** | Elena Rostova | `9876` | ₹24,000.00 |

*Admin Passcode*: `9999`

---

## 🧪 Running Unit Tests

Run the test suite via the test runner:
```bash
python3 run_tests.py
```
Or directly using Python's test discovery:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 License
This project is open-source and distributed under the MIT License.
