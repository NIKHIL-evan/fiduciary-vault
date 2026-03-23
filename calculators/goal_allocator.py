from schemas.user_profile import UserFinancialProfile
from calculators.investable_surplus import calculate_investable_surplus

def allocate_surplus(user: UserFinancialProfile, surplus: float) -> dict:
    if surplus <= 0:
        return {
            "status": "NO_SURPLUS",
            "message": "No surplus available for allocation.",
            "allocations": {}
        }
    
    allocations = {}
    remaining = surplus
    
    # Step 1: Emergency fund first
    monthly_expenses = user.monthly_expense + sum(
        m.monthly_expense for m in user.family_members if m.is_dependent
    )
    required_emergency = monthly_expenses * 6
    liquid_assets = sum(
        a.estimated_value for a in user.illiquid_assets
        if a.liquidity_score >= 7
    )
    emergency_gap = max(0, required_emergency - liquid_assets)
    
    if emergency_gap > 0:
        emergency_allocation = min(remaining * 0.3, emergency_gap)
        allocations["emergency_fund"] = round(emergency_allocation)
        remaining -= emergency_allocation

    # Step 2: Liquidity events (upcoming needs)
    for event in user.liquidity_events:
        years_left = event.target_year - 2026
        if years_left <= 3 and remaining > 0:
            monthly_needed = event.amount_needed / max(years_left * 12, 1)
            allocation = min(remaining * 0.2, monthly_needed)
            allocations[f"goal_{event.purpose}"] = round(allocation)
            remaining -= allocation

    # Step 3: High interest debt clearance
    high_interest = [d for d in user.existing_debts if d.interest_rate > 12]
    if high_interest and remaining > 0:
        debt_allocation = remaining * 0.5
        allocations["debt_clearance"] = round(debt_allocation)
        remaining -= debt_allocation

    # Step 4: Tax saving (80C gap)
    annual_80c_used = sum(
        i.annual_amount for i in user.existing_investments
        if i.investment_type in ["PPF", "ELSS", "NPS", "NSC"]
    )
    remaining_80c = max(0, 150000 - annual_80c_used)
    monthly_80c_gap = remaining_80c / 12
    if monthly_80c_gap > 0 and remaining > 0 and user.tax_regime == "old":
        tax_allocation = min(remaining * 0.2, monthly_80c_gap)
        allocations["tax_saving"] = round(tax_allocation)
        remaining -= tax_allocation

    # Step 5: Wealth building with remainder
    if remaining > 0:
        allocations["wealth_building"] = round(remaining)

    return {
        "status": "ALLOCATED",
        "total_surplus": surplus,
        "allocations": allocations,
        "priority_order": list(allocations.keys())
    }