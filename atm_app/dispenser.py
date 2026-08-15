"""Cash dispenser engine simulating ATM banknote cassettes and greedy dispense."""
from typing import Dict
from atm_app.exceptions import CashDispenserError

class CashDispenser:
    SUPPORTED_DENOMINATIONS = [2000, 500, 200, 100]

    def __init__(self, initial_cash: Dict[int, int] | None = None):
        if initial_cash is None:
            # Default cash inventory in ATM
            self.cassettes = {2000: 25, 500: 50, 200: 100, 100: 150}
        else:
            self.cassettes = initial_cash

    @property
    def total_cash_available(self) -> int:
        return sum(denom * count for denom, count in self.cassettes.items())

    def can_dispense(self, amount: int) -> bool:
        try:
            self._calculate_dispense(amount)
            return True
        except CashDispenserError:
            return False

    def _calculate_dispense(self, amount: int) -> Dict[int, int]:
        if amount <= 0 or amount % 100 != 0:
            raise CashDispenserError("Withdrawal must be a multiple of ₹100.")

        if amount > self.total_cash_available:
            raise CashDispenserError("ATM machine has insufficient cash reserve.")

        remaining = amount
        dispense_plan: Dict[int, int] = {}
        for denom in sorted(self.cassettes.keys(), reverse=True):
            available_notes = self.cassettes.get(denom, 0)
            if available_notes > 0 and remaining >= denom:
                notes_needed = remaining // denom
                notes_to_take = min(notes_needed, available_notes)
                if notes_to_take > 0:
                    dispense_plan[denom] = notes_to_take
                    remaining -= notes_to_take * denom

        if remaining != 0:
            raise CashDispenserError("ATM cannot dispense exact denominations for this amount.")
        return dispense_plan

    def dispense(self, amount: int) -> Dict[int, int]:
        """Calculates notes and deducts them from cassette inventory."""
        plan = self._calculate_dispense(amount)
        for denom, count in plan.items():
            self.cassettes[denom] -= count
        return plan

    def refill(self, new_notes: Dict[int, int]) -> None:
        """Admin refill of notes into cassettes."""
        for denom, count in new_notes.items():
            if denom in self.cassettes:
                self.cassettes[denom] += count
            else:
                self.cassettes[denom] = count
