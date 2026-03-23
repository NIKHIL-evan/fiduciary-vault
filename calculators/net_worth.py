from schemas.user_profile import UserFinancialProfile

def calculate_net_worth(user: UserFinancialProfile) -> dict:
    
    # ASSETS
    # Liquid investments
    investment_value = sum(
        i.annual_amount for i in user.existing_investments
    )
    
    # Illiquid assets
    illiquid_value = sum(
        a.estimated_value for a in user.illiquid_assets
    )
    
    # EPF balance
    epf_value = user.epf_balance
    
    # ESOP/RSU value
    esop_value = user.esop_rsu_value
    
    # Insurance policies surrender value
    policy_value = sum(
        p.surrender_value for p in user.existing_policies
    )
    
    total_assets = investment_value + illiquid_value + epf_value + esop_value + policy_value
    
    # LIABILITIES
    total_debt = sum(d.amount for d in user.existing_debts)
    
    # NET WORTH
    net_worth = total_assets - total_debt
    
    # Life stage benchmark (rough Indian middle class benchmarks)
    age = user.age
    annual_income = user.monthly_income * 12
    expected_net_worth = annual_income * ((age - 25) / 10)
    
    if net_worth >= expected_net_worth:
        health = "ON TRACK"
    elif net_worth >= expected_net_worth * 0.5:
        health = "BELOW TARGET"
    else:
        health = "SIGNIFICANTLY BEHIND"
    
    return {
        "total_assets": round(total_assets),
        "total_liabilities": round(total_debt),
        "net_worth": round(net_worth),
        "expected_net_worth": round(expected_net_worth),
        "net_worth_health": health,
        "asset_breakdown": {
            "investments": round(investment_value),
            "illiquid_assets": round(illiquid_value),
            "epf": round(epf_value),
            "esop_rsu": round(esop_value),
            "policy_surrender_value": round(policy_value)
        },
        "debt_breakdown": round(total_debt)
    }