from schemas.user_profile import UserFinancialProfile

def calculate_emergency_fund(user: UserFinancialProfile) -> dict:
    monthly_expenses = user.monthly_expense + sum(
        m.monthly_expense for m in user.family_members if m.is_dependent
    )
    
    # Required: 6 months for employed, 12 months for self-employed
    required_months = 6
    required_amount = monthly_expenses * required_months
    
    # Current liquid assets (liquidity score >= 7)
    current_liquid = sum(
        a.estimated_value for a in user.illiquid_assets
        if a.liquidity_score >= 7
    )
    
    gap = max(0, required_amount - current_liquid)
    months_covered = current_liquid / monthly_expenses if monthly_expenses > 0 else 0
    
    if months_covered >= 6:
        status = "ADEQUATE"
        message = f"Emergency fund covers {round(months_covered, 1)} months. You are protected."
    elif months_covered >= 3:
        status = "PARTIAL"
        message = f"Emergency fund covers only {round(months_covered, 1)} months. Target 6 months."
    else:
        status = "CRITICAL"
        message = f"Emergency fund covers only {round(months_covered, 1)} months. This is dangerous."
    
    return {
        "status": status,
        "monthly_expenses": monthly_expenses,
        "required_amount": required_amount,
        "current_liquid": current_liquid,
        "gap": round(gap),
        "months_covered": round(months_covered, 1),
        "message": message,
        "monthly_saving_needed": round(gap / 12) if gap > 0 else 0
    }