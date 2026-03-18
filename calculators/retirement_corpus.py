def calculate_retirement_corpus(
    monthly_expense: float,
    current_age: int,
    retirement_age: int,
    inflation_rate: float = 0.06,
    post_retirement_years: int = 25,
    safe_withdrawal_rate: float = 0.04
) -> dict:
    years_to_retirement = retirement_age - current_age
    
    future_monthly_expense = monthly_expense * ((1 + inflation_rate) ** years_to_retirement)
    future_annual_expense = future_monthly_expense * 12
    corpus_needed = future_annual_expense / safe_withdrawal_rate
    
    return {
        "years_to_retirement": years_to_retirement,
        "future_monthly_expense": round(future_monthly_expense, 2),
        "corpus_needed": round(corpus_needed, 2)
    }


