from schemas.user_profile import UserFinancialProfile
from calculators.investable_surplus import calculate_investable_surplus
from calculators.emergency_fund import calculate_emergency_fund
from calculators.net_worth import calculate_net_worth
from calculators.risk_profiler import calculate_risk_profile

def calculate_financial_health_score(user: UserFinancialProfile) -> dict:
    score = 0
    breakdown = {}
    
    # 1. CASH FLOW (25 points)
    surplus = calculate_investable_surplus(user)
    monthly_income = user.monthly_income
    surplus_ratio = surplus / monthly_income if monthly_income > 0 else 0
    
    if surplus_ratio >= 0.3:
        cf_score = 25
    elif surplus_ratio >= 0.1:
        cf_score = 15
    elif surplus_ratio >= 0:
        cf_score = 5
    else:
        cf_score = 0
    
    score += cf_score
    breakdown["cash_flow"] = {
        "score": cf_score,
        "max": 25,
        "detail": f"Surplus: ₹{round(surplus)} ({round(surplus_ratio*100)}% of income)"
    }
    
    # 2. EMERGENCY FUND (20 points)
    emergency = calculate_emergency_fund(user)
    if emergency["months_covered"] >= 6:
        ef_score = 20
    elif emergency["months_covered"] >= 3:
        ef_score = 10
    else:
        ef_score = 0
    
    score += ef_score
    breakdown["emergency_fund"] = {
        "score": ef_score,
        "max": 20,
        "detail": f"{emergency['months_covered']} months covered"
    }
    
    # 3. DEBT HEALTH (20 points)
    high_interest = [d for d in user.existing_debts if d.interest_rate > 12]
    if not user.existing_debts:
        debt_score = 20
    elif not high_interest:
        debt_score = 15
    elif len(high_interest) == 1:
        debt_score = 5
    else:
        debt_score = 0
    
    score += debt_score
    breakdown["debt_health"] = {
        "score": debt_score,
        "max": 20,
        "detail": f"{len(high_interest)} high-interest debts detected"
    }
    
    # 4. INSURANCE COVERAGE (15 points)
    required_term = user.monthly_income * 12 * 10
    has_dependents = any(m.is_dependent for m in user.family_members)
    
    if not has_dependents:
        ins_score = 15
    elif user.term_insurance_cover >= required_term:
        ins_score = 15
    elif user.term_insurance_cover >= required_term * 0.5:
        ins_score = 7
    else:
        ins_score = 0
    
    score += ins_score
    breakdown["insurance"] = {
        "score": ins_score,
        "max": 15,
        "detail": f"Term cover: ₹{round(user.term_insurance_cover/100000)}L of ₹{round(required_term/100000)}L required"
    }
    
    # 5. RETIREMENT READINESS (20 points)
    nw = calculate_net_worth(user)
    if nw["net_worth_health"] == "ON TRACK":
        ret_score = 20
    elif nw["net_worth_health"] == "BELOW TARGET":
        ret_score = 10
    else:
        ret_score = 0
    
    score += ret_score
    breakdown["retirement"] = {
        "score": ret_score,
        "max": 20,
        "detail": nw["net_worth_health"]
    }
    
    # FINAL GRADE
    if score >= 80:
        grade = "A"
        status = "EXCELLENT"
    elif score >= 60:
        grade = "B"
        status = "GOOD"
    elif score >= 40:
        grade = "C"
        status = "NEEDS IMPROVEMENT"
    else:
        grade = "D"
        status = "CRITICAL"
    
    return {
        "total_score": score,
        "max_score": 100,
        "grade": grade,
        "status": status,
        "breakdown": breakdown,
        "summary": f"Financial Health: {score}/100 ({grade}) — {status}"
    }
