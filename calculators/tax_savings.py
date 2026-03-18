SECTION_80C_LIMIT = 150000
ELIGIBLE_80C_INVESTMENTS = ["PPF", "ELSS", "NSC", "tax_fd", "NPS"]

def calculate_tax_savings(
    annual_income: float,
    existing_investments: list,
    tax_regime: str
) -> dict:
    if tax_regime == "new":
        return {
            "regime": "new",
            "message": "No 80C deductions in new regime.",
            "tax_saved": 0,
            "remaining_80c_limit": 0
        }
    
    used_80c = sum(
        inv.annual_amount 
        for inv in existing_investments 
        if inv.investment_type in ELIGIBLE_80C_INVESTMENTS
    )
    
    remaining_80c = max(0, SECTION_80C_LIMIT - used_80c)
    tax_saved = remaining_80c * 0.30
    
    return {
        "regime": "old",
        "used_80c": used_80c,
        "remaining_80c": remaining_80c,
        "tax_saved": round(tax_saved, 2)
    }