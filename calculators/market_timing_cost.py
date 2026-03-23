def calculate_market_timing_cost(
    monthly_sip: float,
    months_waiting: int,
    expected_return: float = 12.0,
    inflation_rate: float = 6.0
) -> dict:
    
    monthly_rate = expected_return / (12 * 100)
    total_years = 20
    total_months = total_years * 12
    
    # If invest now
    corpus_if_now = monthly_sip * (
        ((1 + monthly_rate)**total_months - 1) / monthly_rate
    )
    
    # If wait N months
    remaining_months = total_months - months_waiting
    corpus_if_wait = monthly_sip * (
        ((1 + monthly_rate)**remaining_months - 1) / monthly_rate
    )
    
    corpus_lost = corpus_if_now - corpus_if_wait
    
    # Cash sitting idle loses to inflation
    cash_idle = monthly_sip * months_waiting
    inflation_erosion = cash_idle * (inflation_rate / 100) * (months_waiting / 12)
    
    total_cost = corpus_lost + inflation_erosion
    
    return {
        "monthly_sip": monthly_sip,
        "months_waiting": months_waiting,
        "corpus_if_invest_now": round(corpus_if_now),
        "corpus_if_wait": round(corpus_if_wait),
        "corpus_lost_by_waiting": round(corpus_lost),
        "inflation_erosion_on_idle_cash": round(inflation_erosion),
        "total_cost_of_waiting": round(total_cost),
        "recommendation": f"Waiting {months_waiting} months costs ₹{round(total_cost/100000)}L in lost wealth. Market timing is a myth — start SIP today."
    }