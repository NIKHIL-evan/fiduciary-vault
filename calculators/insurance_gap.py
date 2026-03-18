MINIMUM_HEALTH_COVER = 1000000  # ₹10 Lakh
INCOME_MULTIPLIER = 10  # thumb rule for term insurance

def calculate_insurance_gap(
    monthly_income: float,
    term_insurance_cover: float,
    health_insurance_cover: float,
    has_dependents: bool
) -> dict:
    annual_income = monthly_income * 12
    required_term_cover = annual_income * INCOME_MULTIPLIER
    term_gap = max(0, required_term_cover - term_insurance_cover)
    health_gap = max(0, MINIMUM_HEALTH_COVER - health_insurance_cover)

    return {
        "required_term_cover": required_term_cover,
        "current_term_cover": term_insurance_cover,
        "term_gap": term_gap,
        "health_gap": health_gap,
        "critical": has_dependents and term_gap > 0
    }