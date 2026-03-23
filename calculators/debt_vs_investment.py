def calculate_debt_vs_investment(
    loan_amount: float,
    loan_rate: float,
    investment_return: float,
    tax_bracket: float,
    is_home_loan: bool = False,
    home_loan_interest_paid: float = 0
) -> dict:
    
    # Effective loan rate after tax benefit
    if is_home_loan:
        # Section 24(b) — up to ₹2L deduction
        deductible = min(home_loan_interest_paid, 200000)
        tax_saved = deductible * (tax_bracket / 100)
        effective_rate = loan_rate - (tax_saved / loan_amount * 100)
    else:
        effective_rate = loan_rate
    
    # Post-tax investment return
    if investment_return > 12:
        # Equity — LTCG at 12.5% above ₹1.25L
        post_tax_return = investment_return - (investment_return * 0.125)
    else:
        # Debt — taxed at slab rate
        post_tax_return = investment_return - (investment_return * tax_bracket / 100)
    
    verdict = "INVEST" if post_tax_return > effective_rate else "PREPAY"
    
    advantage = abs(post_tax_return - effective_rate)
    
    annual_benefit = loan_amount * (advantage / 100)
    
    return {
        "loan_rate": loan_rate,
        "effective_loan_rate": round(effective_rate, 2),
        "investment_return": investment_return,
        "post_tax_investment_return": round(post_tax_return, 2),
        "verdict": verdict,
        "advantage_percent": round(advantage, 2),
        "annual_benefit": round(annual_benefit),
        "reasoning": f"Effective debt cost {round(effective_rate,2)}% vs post-tax investment return {round(post_tax_return,2)}% — {verdict} wins by {round(advantage,2)}%"
    }