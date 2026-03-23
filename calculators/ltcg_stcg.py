def calculate_capital_gains_tax(
    purchase_value: float,
    sale_value: float,
    holding_months: int,
    asset_type: str,  # "equity", "debt", "gold"
    tax_bracket: float = 30
) -> dict:
    gain = sale_value - purchase_value
    
    if gain <= 0:
        return {
            "gain": round(gain),
            "tax_owed": 0,
            "gain_type": "LOSS",
            "recommendation": f"Capital loss of ₹{abs(round(gain))} — can be used to offset other gains"
        }
    
    if asset_type == "equity":
        if holding_months < 12:
            gain_type = "STCG"
            tax_rate = 20
            tax_owed = gain * 0.20
        else:
            gain_type = "LTCG"
            exemption = 125000
            taxable_gain = max(0, gain - exemption)
            tax_rate = 12.5
            tax_owed = taxable_gain * 0.125
            
    elif asset_type == "debt":
        gain_type = "Debt Fund Gains"
        tax_rate = tax_bracket
        tax_owed = gain * (tax_bracket / 100)
        
    elif asset_type == "gold":
        if holding_months < 36:
            gain_type = "STCG"
            tax_rate = tax_bracket
            tax_owed = gain * (tax_bracket / 100)
        else:
            gain_type = "LTCG"
            tax_rate = 20
            tax_owed = gain * 0.20

    return {
        "purchase_value": purchase_value,
        "sale_value": sale_value,
        "gain": round(gain),
        "holding_months": holding_months,
        "gain_type": gain_type,
        "tax_rate_percent": tax_rate,
        "tax_owed": round(tax_owed),
        "post_tax_gain": round(gain - tax_owed),
        "recommendation": f"Selling triggers {gain_type} tax of ₹{round(tax_owed)} at {tax_rate}%"
    }