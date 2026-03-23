def calculate_education_goal(
    child_age: int,
    education_start_age: int = 18,
    current_cost: float = 1500000,
    inflation_rate: float = 8.0,
    expected_return: float = 12.0
) -> dict:
    
    years_to_goal = education_start_age - child_age
    
    if years_to_goal <= 0:
        return {
            "status": "IMMEDIATE",
            "message": "Education starting now. Need lump sum immediately.",
            "amount_needed": current_cost
        }
    
    # Future cost of education
    future_cost = current_cost * ((1 + inflation_rate/100) ** years_to_goal)
    
    # Monthly SIP required
    monthly_rate = expected_return / (12 * 100)
    months = years_to_goal * 12
    
    monthly_sip = (future_cost * monthly_rate) / ((1 + monthly_rate)**months - 1)
    
    # Asset allocation based on timeline
    if years_to_goal > 7:
        allocation = "70% Equity Index Fund + 30% Debt Fund"
    elif years_to_goal > 3:
        allocation = "40% Equity + 60% Balanced Advantage Fund"
    else:
        allocation = "100% Liquid/Short Duration Debt Fund"
    
    return {
        "child_age": child_age,
        "years_to_goal": years_to_goal,
        "current_cost": current_cost,
        "future_cost": round(future_cost),
        "monthly_sip_required": round(monthly_sip),
        "recommended_allocation": allocation,
        "recommendation": f"Start ₹{round(monthly_sip)}/month SIP now for {child_age}-year-old's education in {years_to_goal} years"
    }