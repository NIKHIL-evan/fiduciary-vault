from schemas.user_profile import UserFinancialProfile

def calculate_investable_surplus(user: UserFinancialProfile) -> float:
    total_exp = user.monthly_expense + sum(m.monthly_expense for m in user.family_members if m.is_dependent)

    total_debt = sum(d.min_payment for d in user.existing_debts)
    surplus = user.monthly_income - total_exp - total_debt
    return surplus