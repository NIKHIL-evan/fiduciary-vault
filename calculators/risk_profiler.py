from schemas.user_profile import UserFinancialProfile

def calculate_risk_profile(user: UserFinancialProfile) -> dict:
    score = 0
    
    # Age factor (younger = can take more risk)
    if user.age < 30: score += 30
    elif user.age < 40: score += 20
    elif user.age < 50: score += 10
    else: score += 0
    
    # Dependents factor
    dependents = [m for m in user.family_members if m.is_dependent]
    if len(dependents) == 0: score += 20
    elif len(dependents) <= 2: score += 10
    else: score += 0
    
    # Debt factor
    high_interest_debt = any(d.interest_rate > 12 for d in user.existing_debts)
    if not high_interest_debt: score += 20
    else: score += 0
    
    # Emergency fund factor
    monthly_expenses = user.monthly_expense + sum(
        m.monthly_expense for m in user.family_members if m.is_dependent
    )
    emergency_fund = sum(
        a.estimated_value for a in user.illiquid_assets 
        if a.liquidity_score >= 7
    )
    months_covered = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
    if months_covered >= 6: score += 20
    elif months_covered >= 3: score += 10
    else: score += 0
    
    # Investment horizon factor
    years_to_retirement = user.retirement_age - user.age
    if years_to_retirement > 20: score += 10
    elif years_to_retirement > 10: score += 5
    else: score += 0
    
    # Determine profile
    if score >= 70:
        profile = "AGGRESSIVE"
        description = "Can handle high volatility. Focus on equity for maximum growth."
    elif score >= 40:
        profile = "MODERATE"
        description = "Balanced approach. Mix of equity and debt."
    else:
        profile = "CONSERVATIVE"
        description = "Capital protection priority. Focus on stable returns."
    
    return {
        "risk_score": score,
        "risk_profile": profile,
        "description": description,
        "years_to_retirement": years_to_retirement
    }