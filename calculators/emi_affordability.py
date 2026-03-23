def calculate_emi_affordability(
    monthly_income: float,
    proposed_emi: float,
    existing_emis: float = 0,
    property_price: float = 0,
    annual_income: float = 0
) -> dict:
    
    total_emi = proposed_emi + existing_emis
    emi_to_income_ratio = (total_emi / monthly_income) * 100
    
    # 30-30-3 rule
    safe_emi_limit = monthly_income * 0.30
    recommended_down_payment = property_price * 0.30 if property_price else 0
    affordable_property_price = annual_income * 3 if annual_income else 0
    
    violations = []
    
    # Rule 1: EMI ≤ 30% of income
    if emi_to_income_ratio > 30:
        violations.append(
            f"EMI is {round(emi_to_income_ratio)}% of income — exceeds 30% safe limit of ₹{round(safe_emi_limit)}/month"
        )
    
    # Rule 3: Property price ≤ 3x annual income
    if property_price and affordable_property_price and property_price > affordable_property_price:
        violations.append(
            f"Property ₹{round(property_price/100000)}L exceeds 3x annual income limit of ₹{round(affordable_property_price/100000)}L"
        )
    
    verdict = "BLOCKED" if violations else "APPROVED"
    
    return {
        "proposed_emi": proposed_emi,
        "existing_emis": existing_emis,
        "total_emi_burden": round(total_emi),
        "emi_to_income_ratio": round(emi_to_income_ratio, 1),
        "safe_emi_limit": round(safe_emi_limit),
        "recommended_down_payment": round(recommended_down_payment),
        "affordable_property_price": round(affordable_property_price),
        "verdict": verdict,
        "violations": violations,
        "recommendation": f"BLOCKED — {'. '.join(violations)}" if violations
            else f"APPROVED — EMI is {round(emi_to_income_ratio)}% of income, within safe 30% limit"
    }

def calculate_purchase_affordability(
    purchase_amount: float,
    monthly_surplus: float,
    financial_health_status: str,
    has_emergency_fund: bool
) -> dict:
    
    months_to_save = purchase_amount / monthly_surplus if monthly_surplus > 0 else 999
    
    if financial_health_status == "EMERGENCY":
        verdict = "BLOCKED"
        reason = "Financial emergency — no discretionary spending"
    elif not has_emergency_fund:
        verdict = "BLOCKED"
        reason = "Build emergency fund first before discretionary purchases"
    elif months_to_save > 3:
        verdict = "CAUTION"
        reason = f"Takes {round(months_to_save)} months of surplus — consider waiting"
    else:
        verdict = "APPROVED"
        reason = f"Affordable — saves in {round(months_to_save)} months"
    
    return {
        "purchase_amount": purchase_amount,
        "monthly_surplus": monthly_surplus,
        "months_to_save": round(months_to_save),
        "verdict": verdict,
        "reason": reason,
        "recommendation": f"{verdict}: {reason}"
    }
