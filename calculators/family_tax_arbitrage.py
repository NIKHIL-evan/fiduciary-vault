def calculate_family_tax_arbitrage(
    investment_amount: float,
    investment_return_percent: float,
    user_tax_bracket: float,
    family_member_tax_bracket: float,
    family_member_relation: str
) -> dict:
    
    annual_return = investment_amount * (investment_return_percent / 100)
    
    # Tax paid by user
    user_tax = annual_return * (user_tax_bracket / 100)
    user_post_tax = annual_return - user_tax
    
    # Tax paid by family member
    family_tax = annual_return * (family_member_tax_bracket / 100)
    family_post_tax = annual_return - family_tax
    
    annual_saving = user_tax - family_tax
    ten_year_saving = annual_saving * 10
    
    is_eligible = family_member_relation.lower() in [
        "parent", "spouse", "sibling", "child", 
        "grandparent", "in-law"
    ]
    
    return {
        "investment_amount": investment_amount,
        "annual_return": round(annual_return),
        "user_tax_bracket": user_tax_bracket,
        "family_member_tax_bracket": family_member_tax_bracket,
        "user_tax_on_interest": round(user_tax),
        "family_tax_on_interest": round(family_tax),
        "annual_tax_saving": round(annual_saving),
        "ten_year_saving": round(ten_year_saving),
        "is_gift_tax_free": is_eligible,
        "recommendation": f"Gift ₹{round(investment_amount)} to your {family_member_relation} → save ₹{round(annual_saving)}/year in tax legally under Section 56"
            if is_eligible and annual_saving > 0
            else "No arbitrage opportunity or ineligible relation"
    }