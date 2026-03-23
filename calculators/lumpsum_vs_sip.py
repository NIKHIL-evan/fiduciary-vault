def calculate_lumpsum_vs_sip(
    amount: float,
    years: int,
    expected_return: float = 12.0,
    sip_months: int = 12
) -> dict:
    
    monthly_rate = expected_return / (12 * 100)
    annual_rate = expected_return / 100
    
    # Lumpsum future value
    lumpsum_fv = amount * (1 + annual_rate) ** years
    
    # STP: Park in liquid fund, transfer monthly to equity
    monthly_sip = amount / sip_months
    sip_fv = 0
    
    for month in range(sip_months):
        months_remaining = (years * 12) - month
        sip_fv += monthly_sip * (1 + monthly_rate) ** months_remaining
    
    # Liquid fund return on remaining amount
    liquid_rate = 7.0 / (12 * 100)
    liquid_fv = 0
    remaining = amount
    for month in range(sip_months):
        liquid_fv += remaining * liquid_rate
        remaining -= monthly_sip
    
    total_stp_fv = sip_fv + liquid_fv
    
    verdict = "LUMPSUM" if lumpsum_fv > total_stp_fv else "STP"
    difference = abs(lumpsum_fv - total_stp_fv)
    
    return {
        "amount": amount,
        "years": years,
        "lumpsum_future_value": round(lumpsum_fv),
        "stp_future_value": round(total_stp_fv),
        "difference": round(difference),
        "verdict": verdict,
        "recommendation": f"In a stable/rising market → LUMPSUM. In volatile market → STP over {sip_months} months. Difference: ₹{round(difference/100000)}L"
    }