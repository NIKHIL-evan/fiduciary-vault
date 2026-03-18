from schemas.user_profile import DebtProfile
from typing import List

def calculate_avalanche_payment(debts: List[DebtProfile], surplus: float) -> dict:
    if surplus <= 0:
        return {"extra_payment_to": None, "amount": 0, "reason": "No surplus available"}
    
    highest_interest_debt = max(debts, key=lambda d: d.interest_rate)
    
    return {
        "extra_payment_to": highest_interest_debt.debt_type,
        "amount": surplus,
        "reason": f"Paying extra ₹{surplus} to {highest_interest_debt.debt_type} at {highest_interest_debt.interest_rate}% first. Saves most interest."
    }