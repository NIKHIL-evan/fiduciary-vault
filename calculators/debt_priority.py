from schemas.user_profile import DebtProfile

def should_clear_debt(user: DebtProfile):
    ESTIMATED_SIP_RETURN = 12
    return user.interest_rate > ESTIMATED_SIP_RETURN

