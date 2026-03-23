def calculate_esop_tax(
    vesting_value: float,
    purchase_price: float,
    tax_bracket: float,
    holding_months_after_vest: int = 0
) -> dict:
    
    # Perquisite tax at vesting
    perquisite_gain = vesting_value - purchase_price
    perquisite_tax = perquisite_gain * (tax_bracket / 100)
    
    # Capital gains if sold after vesting
    if holding_months_after_vest < 12:
        cg_tax_rate = 20
        cg_tax = vesting_value * 0.20
        cg_type = "STCG"
    else:
        cg_tax_rate = 12.5
        cg_tax = max(0, vesting_value - 125000) * 0.125
        cg_type = "LTCG"
    
    total_tax = perquisite_tax
    
    return {
        "vesting_value": vesting_value,
        "purchase_price": purchase_price,
        "perquisite_gain": round(perquisite_gain),
        "perquisite_tax": round(perquisite_tax),
        "tax_bracket": tax_bracket,
        "immediate_tax_owed": round(perquisite_tax),
        "if_sold_now_additional_tax": round(cg_tax),
        "total_tax_if_sold_now": round(perquisite_tax + cg_tax),
        "recommendation": f"₹{round(perquisite_tax)} tax owed immediately on vesting. Sell enough shares to cover tax bill. Diversify remaining into index funds."
    }