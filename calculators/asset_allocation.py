def calculate_asset_allocation(
    age: int,
    risk_profile: str,
    investment_horizon_years: int,
    monthly_surplus: float
) -> dict:
    
    # Base equity allocation by age (100 - age rule, modified)
    base_equity = min(90, max(30, 110 - age))
    
    # Adjust for risk profile
    if risk_profile == "CONSERVATIVE":
        equity = base_equity - 20
    elif risk_profile == "AGGRESSIVE":
        equity = base_equity + 10
    else:
        equity = base_equity
    
    equity = max(20, min(90, equity))
    
    # Adjust for horizon
    if investment_horizon_years < 3:
        equity = min(equity, 20)
    elif investment_horizon_years < 5:
        equity = min(equity, 50)
    
    debt = max(10, 90 - equity)
    gold = 10
    
    # Normalize
    total = equity + debt + gold
    equity = round(equity / total * 100)
    debt = round(debt / total * 100)
    gold = 100 - equity - debt
    
    # Fund recommendations
    if equity > 60:
        equity_funds = "Nifty 50 Index Fund (60%) + Flexi Cap Fund (40%)"
    elif equity > 40:
        equity_funds = "Balanced Advantage Fund (60%) + Nifty 50 Index (40%)"
    else:
        equity_funds = "Conservative Hybrid Fund"
    
    return {
        "age": age,
        "risk_profile": risk_profile,
        "horizon_years": investment_horizon_years,
        "equity_percent": equity,
        "debt_percent": debt,
        "gold_percent": gold,
        "equity_allocation": round(monthly_surplus * equity / 100),
        "debt_allocation": round(monthly_surplus * debt / 100),
        "gold_allocation": round(monthly_surplus * gold / 100),
        "recommended_funds": equity_funds,
        "recommendation": f"Age {age}, {risk_profile} profile → {equity}% Equity, {debt}% Debt, {gold}% Gold"
    }