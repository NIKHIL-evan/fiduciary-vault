def estimate_insurance_premium(
    cover_amount: float,
    age: int,
    policy_type: str,  # "term", "health_individual", "health_family"
    tenure_years: int = 30,
    family_size: int = 1
) -> dict:
    
    if policy_type == "term":
        # Base rate per ₹1Cr cover per year
        if age < 30:
            base_rate = 0.008
        elif age < 35:
            base_rate = 0.010
        elif age < 40:
            base_rate = 0.014
        elif age < 45:
            base_rate = 0.020
        else:
            base_rate = 0.030
        
        annual_premium = cover_amount * base_rate
        premium_type = "Term Life Insurance"
        
    elif policy_type == "health_individual":
        if age < 30:
            annual_premium = 8000
        elif age < 40:
            annual_premium = 12000
        elif age < 50:
            annual_premium = 18000
        else:
            annual_premium = 28000
            
        # Scale for cover amount
        if cover_amount > 1000000:
            annual_premium *= (cover_amount / 1000000)
        premium_type = "Individual Health Insurance"
        
    elif policy_type == "health_family":
        base = 15000 if age < 35 else 22000
        annual_premium = base + (family_size - 1) * 5000
        if cover_amount > 2000000:
            annual_premium *= (cover_amount / 2000000)
        premium_type = "Family Floater Health Insurance"
    
    else:
        annual_premium = 0
        premium_type = "Unknown"
    
    return {
        "policy_type": premium_type,
        "cover_amount": cover_amount,
        "age": age,
        "estimated_annual_premium": round(annual_premium),
        "estimated_monthly_premium": round(annual_premium / 12),
        "note": "These are estimated ranges. Actual premium depends on health history and insurer.",
        "recommendation": f"Budget ₹{round(annual_premium/12)}/month for {premium_type} of ₹{round(cover_amount/100000)}L"
    }