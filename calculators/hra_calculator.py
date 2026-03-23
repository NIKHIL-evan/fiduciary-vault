def calculate_hra_exemption(
    basic_salary_annual: float,
    hra_received_annual: float,
    rent_paid_annual: float,
    is_metro: bool = True
) -> dict:
    
    # Three conditions
    condition_1 = hra_received_annual
    condition_2 = rent_paid_annual - (0.10 * basic_salary_annual)
    condition_3 = basic_salary_annual * (0.50 if is_metro else 0.40)
    
    # Exempt = minimum of three
    hra_exempt = max(0, min(condition_1, condition_2, condition_3))
    hra_taxable = hra_received_annual - hra_exempt
    
    return {
        "basic_salary_annual": basic_salary_annual,
        "hra_received_annual": hra_received_annual,
        "rent_paid_annual": rent_paid_annual,
        "city_type": "Metro" if is_metro else "Non-Metro",
        "condition_1_actual_hra": round(condition_1),
        "condition_2_rent_minus_10_percent": round(condition_2),
        "condition_3_percent_of_basic": round(condition_3),
        "hra_exempt": round(hra_exempt),
        "hra_taxable": round(hra_taxable),
        "recommendation": f"₹{round(hra_exempt)} of your HRA is tax-exempt. Claim this in your ITR."
    }