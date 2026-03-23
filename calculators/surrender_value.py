def calculate_surrender_benefit(
    policy_type: str,
    annual_premium: float,
    years_paid: int,
    surrender_value: float,
    maturity_value: float,
    years_to_maturity: int,
    alternative_return_percent: float = 12.0
) -> dict:
    
    # What you get if you continue
    total_premiums_remaining = annual_premium * years_to_maturity
    net_maturity_gain = maturity_value - (annual_premium * (years_paid + years_to_maturity))
    
    # CAGR of policy
    total_invested = annual_premium * (years_paid + years_to_maturity)
    if total_invested > 0 and years_to_maturity > 0:
        policy_cagr = ((maturity_value / total_invested) ** (1 / (years_paid + years_to_maturity)) - 1) * 100
    else:
        policy_cagr = 0
    
    # What you get if you surrender and reinvest
    import math
    monthly_rate = alternative_return_percent / (12 * 100)
    months = years_to_maturity * 12
    
    # Future value of surrender value invested as lump sum
    fv_surrender = surrender_value * (1 + alternative_return_percent/100) ** years_to_maturity
    
    # Future value of premium redirected to SIP
    fv_premium_sip = annual_premium/12 * (((1 + monthly_rate)**months - 1) / monthly_rate)
    
    total_if_surrender = fv_surrender + fv_premium_sip
    
    net_benefit_of_surrender = total_if_surrender - maturity_value
    
    verdict = "SURRENDER" if net_benefit_of_surrender > 0 else "CONTINUE"
    
    return {
        "policy_type": policy_type,
        "surrender_value": surrender_value,
        "maturity_value": maturity_value,
        "policy_cagr": round(policy_cagr, 2),
        "if_continue": round(maturity_value),
        "if_surrender_and_reinvest": round(total_if_surrender),
        "net_benefit_of_surrender": round(net_benefit_of_surrender),
        "verdict": verdict,
        "recommendation": f"SURRENDER this {policy_type}. Reinvesting gives ₹{round(net_benefit_of_surrender)} more over {years_to_maturity} years"
            if verdict == "SURRENDER"
            else f"Continue this policy. Surrendering costs you ₹{abs(round(net_benefit_of_surrender))}"
    }