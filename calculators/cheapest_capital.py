def calculate_cheapest_capital(
    amount_needed: float,
    mf_portfolio_value: float = 0,
    fd_value: float = 0,
    fd_interest_rate: float = 0,
    fd_months_remaining: int = 0,
    gold_value: float = 0,
    mf_holding_period_months: int = 0,
    mf_gain_percent: float = 0
) -> dict:
    options = []

    # Option 1: LAMF (Loan Against Mutual Funds)
    if mf_portfolio_value >= amount_needed * 0.5:
        lamf_interest = amount_needed * 0.10 / 12  # monthly at 10%
        options.append({
            "option": "LAMF (Loan Against Mutual Funds)",
            "monthly_cost": round(lamf_interest),
            "annual_cost": round(lamf_interest * 12),
            "pros": "Portfolio stays invested, continues growing",
            "cons": "Need to repay loan",
            "recommended_if": "Emergency < 12 months",
            "rank": 1
        })

    # Option 2: Gold Loan
    if gold_value >= amount_needed * 0.7:
        gold_interest = amount_needed * 0.09 / 12  # monthly at 9%
        options.append({
            "option": "Gold Loan",
            "monthly_cost": round(gold_interest),
            "annual_cost": round(gold_interest * 12),
            "pros": "Instant disbursement, low rate",
            "cons": "Gold pledged as collateral",
            "recommended_if": "Need cash within 4 hours",
            "rank": 2
        })

    # Option 3: Break FD
    if fd_value >= amount_needed:
        penalty = fd_value * 0.01  # 1% penalty
        lost_interest = (fd_value * fd_interest_rate / 100 / 12) * fd_months_remaining
        total_cost = penalty + lost_interest
        options.append({
            "option": "Break FD",
            "monthly_cost": 0,
            "annual_cost": round(total_cost),
            "pros": "No ongoing interest",
            "cons": f"Lose ₹{round(total_cost)} in penalty + interest",
            "recommended_if": "Short remaining tenure on FD",
            "rank": 3
        })

    # Option 4: Sell Mutual Funds
    if mf_portfolio_value >= amount_needed:
        if mf_holding_period_months < 12:
            tax_rate = 0.20  # STCG
            tax_type = "STCG (20%)"
        else:
            tax_rate = 0.125  # LTCG above ₹1.25L
            tax_type = "LTCG (12.5%)"
        
        gain = amount_needed * (mf_gain_percent / 100)
        tax_cost = gain * tax_rate
        options.append({
            "option": "Sell Mutual Funds",
            "monthly_cost": 0,
            "annual_cost": round(tax_cost),
            "pros": "Simple, immediate",
            "cons": f"{tax_type} tax of ₹{round(tax_cost)} + loses market position",
            "recommended_if": "Last resort only",
            "rank": 4
        })

    # Sort by rank
    options.sort(key=lambda x: x["rank"])
    
    best = options[0] if options else None

    return {
        "amount_needed": amount_needed,
        "best_option": best["option"] if best else "Personal loan",
        "options_ranked": options,
        "recommendation": f"Use {best['option']} — lowest true cost for your situation" if best else "Consider personal loan at 14-18%"
    }