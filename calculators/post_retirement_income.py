def calculate_post_retirement_income(
    epf_corpus: float = 0,
    ppf_corpus: float = 0,
    nps_corpus: float = 0,
    rental_income_monthly: float = 0,
    other_monthly_income: float = 0,
    withdrawal_rate: float = 4.0
) -> dict:
    
    # Safe withdrawal from EPF/PPF/NPS
    epf_monthly = (epf_corpus * withdrawal_rate / 100) / 12
    ppf_monthly = (ppf_corpus * withdrawal_rate / 100) / 12
    
    # NPS gives 40% as annuity
    nps_annuity_corpus = nps_corpus * 0.40
    nps_monthly = (nps_annuity_corpus * 0.06) / 12  # ~6% annuity rate
    
    total_monthly_income = (
        epf_monthly + ppf_monthly + nps_monthly +
        rental_income_monthly + other_monthly_income
    )
    
    return {
        "epf_monthly_income": round(epf_monthly),
        "ppf_monthly_income": round(ppf_monthly),
        "nps_monthly_income": round(nps_monthly),
        "rental_income": round(rental_income_monthly),
        "other_income": round(other_monthly_income),
        "total_monthly_income": round(total_monthly_income),
        "annual_income": round(total_monthly_income * 12),
        "recommendation": f"Existing sources provide ₹{round(total_monthly_income)}/month post retirement — reduces additional corpus needed"
    }