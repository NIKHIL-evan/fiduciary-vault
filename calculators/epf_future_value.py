def calculate_epf_future_value(
    current_epf_balance: float,
    monthly_salary: float,
    current_age: int,
    retirement_age: int = 60,
    epf_rate: float = 8.25
) -> dict:
    
    years_to_retirement = retirement_age - current_age
    months = years_to_retirement * 12
    
    # Employee contributes 12% of basic (assume basic = 50% of salary)
    basic_salary = monthly_salary * 0.50
    monthly_contribution = basic_salary * 0.12
    employer_contribution = basic_salary * 0.0367  # 3.67% to EPF
    total_monthly = monthly_contribution + employer_contribution
    
    monthly_rate = epf_rate / (12 * 100)
    
    # Future value of current balance
    fv_current = current_epf_balance * (1 + epf_rate/100) ** years_to_retirement
    
    # Future value of monthly contributions
    fv_contributions = total_monthly * (((1 + monthly_rate)**months - 1) / monthly_rate)
    
    total_epf_at_retirement = fv_current + fv_contributions
    
    return {
        "current_epf_balance": current_epf_balance,
        "monthly_epf_contribution": round(total_monthly),
        "epf_interest_rate": epf_rate,
        "years_to_retirement": years_to_retirement,
        "future_value_current_balance": round(fv_current),
        "future_value_contributions": round(fv_contributions),
        "total_epf_at_retirement": round(total_epf_at_retirement),
        "recommendation": f"Your EPF will grow to ₹{round(total_epf_at_retirement/100000)}L by retirement — factor this into corpus planning"
    }