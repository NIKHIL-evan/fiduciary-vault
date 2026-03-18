def calculate_required_sip(
    corpus_needed: float,
    years_to_retirement: int,
    expected_return: float = 0.10
) -> dict:
    months = years_to_retirement * 12
    monthly_rate = expected_return / 12
    
    required_sip = (corpus_needed * monthly_rate) / ((1 + monthly_rate) ** months - 1)
    
    return {
        "corpus_needed": corpus_needed,
        "years_to_retirement": years_to_retirement,
        "required_monthly_sip": round(required_sip, 2)
    }