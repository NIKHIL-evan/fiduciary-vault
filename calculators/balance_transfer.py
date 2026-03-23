def calculate_balance_transfer_benefit(
    current_balance: float,
    current_rate: float,
    new_rate: float,
    transfer_fee_percent: float = 1.5,
    months_remaining: int = 12
) -> dict:
    transfer_fee = current_balance * (transfer_fee_percent / 100)
    
    monthly_old = (current_balance * (current_rate / 100)) / 12
    monthly_new = (current_balance * (new_rate / 100)) / 12
    
    total_interest_old = monthly_old * months_remaining
    total_interest_new = monthly_new * months_remaining
    
    net_saving = total_interest_old - total_interest_new - transfer_fee
    
    return {
        "current_balance": current_balance,
        "current_rate": current_rate,
        "new_rate": new_rate,
        "transfer_fee": round(transfer_fee),
        "monthly_saving": round(monthly_old - monthly_new),
        "total_interest_old": round(total_interest_old),
        "total_interest_new": round(total_interest_new),
        "net_saving": round(net_saving),
        "recommendation": "TRANSFER" if net_saving > 0 else "STAY",
        "breakeven_months": round(transfer_fee / (monthly_old - monthly_new)) if monthly_old > monthly_new else 0
    }