def calculate_tax_harvesting(
    gains: list,  # [{"asset": "Fund A", "gain": 200000, "holding_months": 14}]
    losses: list  # [{"asset": "Fund B", "loss": 50000, "holding_months": 8}]
) -> dict:
    
    total_ltcg = sum(g["gain"] for g in gains if g["holding_months"] >= 12)
    total_stcg = sum(g["gain"] for g in gains if g["holding_months"] < 12)
    total_losses = sum(l["loss"] for l in losses)
    
    # Offset losses against gains
    # STCG losses offset STCG first, then LTCG
    # LTCG losses offset LTCG only
    
    net_ltcg = max(0, total_ltcg - total_losses)
    net_stcg = max(0, total_stcg)
    
    # Tax without harvesting
    ltcg_exemption = 125000
    tax_without_ltcg = max(0, total_ltcg - ltcg_exemption) * 0.125
    tax_without_stcg = total_stcg * 0.20
    tax_without = tax_without_ltcg + tax_without_stcg
    
    # Tax with harvesting
    tax_with_ltcg = max(0, net_ltcg - ltcg_exemption) * 0.125
    tax_with_stcg = net_stcg * 0.20
    tax_with = tax_with_ltcg + tax_with_stcg
    
    tax_saved = tax_without - tax_with
    
    return {
        "total_gains": round(total_ltcg + total_stcg),
        "total_losses_available": round(total_losses),
        "tax_without_harvesting": round(tax_without),
        "tax_with_harvesting": round(tax_with),
        "tax_saved": round(tax_saved),
        "net_ltcg_after_harvesting": round(net_ltcg),
        "net_stcg_after_harvesting": round(net_stcg),
        "recommendation": f"Sell losing positions before March 31 → save ₹{round(tax_saved)} in tax"
            if tax_saved > 0 else "No harvesting opportunity available"
    }