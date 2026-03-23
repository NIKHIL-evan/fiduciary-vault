def calculate_stepup_sip(
    initial_monthly_sip: float,
    annual_stepup_percent: float,
    years: int,
    expected_return: float = 12.0
) -> dict:
    
    monthly_rate = expected_return / (12 * 100)
    total_corpus = 0
    total_invested = 0
    current_sip = initial_monthly_sip
    
    for year in range(years):
        # Each year's SIP contribution
        for month in range(12):
            months_remaining = (years - year) * 12 - month
            fv = current_sip * (1 + monthly_rate) ** months_remaining
            total_corpus += fv
            total_invested += current_sip
        current_sip *= (1 + annual_stepup_percent / 100)
    
    # Compare with flat SIP
    flat_corpus = initial_monthly_sip * (
        ((1 + monthly_rate)**(years*12) - 1) / monthly_rate
    )
    flat_invested = initial_monthly_sip * years * 12
    
    extra_corpus = total_corpus - flat_corpus
    
    return {
        "initial_sip": initial_monthly_sip,
        "annual_stepup_percent": annual_stepup_percent,
        "years": years,
        "final_monthly_sip": round(current_sip),
        "stepup_corpus": round(total_corpus),
        "stepup_total_invested": round(total_invested),
        "flat_corpus": round(flat_corpus),
        "flat_total_invested": round(flat_invested),
        "extra_corpus_from_stepup": round(extra_corpus),
        "recommendation": f"Step-up SIP builds ₹{round(extra_corpus/100000)}L more than flat SIP over {years} years"
    }