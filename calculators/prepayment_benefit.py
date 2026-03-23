import math

def calculate_prepayment_benefit(
    principal: float,
    annual_rate: float,
    tenure_years: int,
    extra_monthly_payment: float
) -> dict:
    monthly_rate = annual_rate / (12 * 100)
    months = tenure_years * 12
    
    # Standard EMI
    emi = (principal * monthly_rate * (1 + monthly_rate)**months) / \
          ((1 + monthly_rate)**months - 1)
    
    # Total payment without prepayment
    total_without = emi * months
    interest_without = total_without - principal
    
    # Calculate months with prepayment
    balance = principal
    months_with_prepayment = 0
    total_paid = 0
    
    while balance > 0:
        interest = balance * monthly_rate
        principal_paid = emi + extra_monthly_payment - interest
        if principal_paid <= 0:
            break
        balance -= principal_paid
        total_paid += emi + extra_monthly_payment
        months_with_prepayment += 1
        if months_with_prepayment > months:
            break
    
    interest_with = total_paid - principal
    months_saved = months - months_with_prepayment
    interest_saved = interest_without - interest_with
    
    return {
        "standard_emi": round(emi),
        "extra_payment": extra_monthly_payment,
        "total_monthly": round(emi + extra_monthly_payment),
        "original_tenure_months": months,
        "new_tenure_months": months_with_prepayment,
        "months_saved": months_saved,
        "years_saved": round(months_saved / 12, 1),
        "interest_without_prepayment": round(interest_without),
        "interest_with_prepayment": round(interest_with),
        "interest_saved": round(interest_saved),
        "recommendation": f"Pay ₹{extra_monthly_payment} extra/month → save ₹{round(interest_saved)} and close {round(months_saved/12, 1)} years early"
    }