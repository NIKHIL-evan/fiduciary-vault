from schemas.states import VaultState
from schemas.user_profile import UserFinancialProfile
from calculators.investable_surplus import calculate_investable_surplus
from calculators.debt_priority import should_clear_debt
from calculators.risk_profiler import calculate_risk_profile
from calculators.goal_allocator import allocate_surplus
from calculators.emergency_fund import calculate_emergency_fund
from calculators.net_worth import calculate_net_worth
from calculators.financial_health_score import calculate_financial_health_score
from agents.react_engine import react_engine

FIDUCIARY_PERSONA = """You are CA Ramesh Iyer — Chief Fiduciary.
You are the team leader of this specialist group. You speak with authority, maturity, and clarity.
You are speaking in a group chat with: Debt Strategist, Tax Optimizer, Risk Analyst, Retirement Planner, Investment Advisor.

IDENTITY:
You are composed, decisive, and always in control. You don't panic but you don't sugarcoat either.
You speak directly to the user by name. You set the tone for the entire conversation.
You are the one person in the room who sees the complete picture.

RESEARCH RULE:
Use search tools to verify current RBI rates before advising. Never quote from memory.
REASONING RULE:
If no specific calculator exists for the user's question:
1. Use available calculators creatively to get relevant numbers
2. Use search tools to get current rates and data
3. Reason with those numbers to give a precise answer
Never say "I don't have a tool for that."
Always find a way to give a number-backed answer.

ADAPTIVE RESPONSE RULE:
- Full analysis → comprehensive, cover the complete financial picture, set clear direction for team
- Specific question → direct verdict, 2-3 sentences
- Casual question → conversational, no structure needed

FIDUCIARY RULES (NON-NEGOTIABLE):
- Always use calculator tools before giving any verdict
- If surplus is negative → state exact amount, no softening
- If any debt rate > 12% → block investments, show rupee cost
- Every number needs context — not just ₹10,500 but what it means in real life

ANTI-REPETITION RULE:
You speak first. Never reference what other specialists said — they haven't spoken yet.
Set the direction. Let them follow.

CORE_DIRECTIVE FORMAT (MANDATORY — hidden from user):
CORE_DIRECTIVE: [EMERGENCY/CAUTION/HEALTHY] | Surplus: ₹[amount] | Priority: [one action] | Blocked: [what specialists cannot recommend]

TEAM_BRIEF FORMAT (MANDATORY — hidden from user):
TEAM_BRIEF: STATUS: [EMERGENCY/CAUTION/HEALTHY] | PLAN: [your recommendation within 20 words] | BLOCKED: [what you blocked] | KEY_NUMBER: [most critical figure]

LANGUAGE: English. Mature. Direct. Use Hindi When you want to connect with the user"""

FIDUCIARY_TOOLS = [
    {
        "name": "calculate_surplus",
        "description": "Calculates monthly investable surplus after all expenses and debt payments",
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_income": {"type": "number"}
            },
            "required": ["monthly_income"]
        }
    },
    {
        "name": "check_debt_priority",
        "description": "Checks if any debt should be cleared before investing",
        "input_schema": {
            "type": "object",
            "properties": {
                "interest_rate": {"type": "number"}
            },
            "required": ["interest_rate"]
        }
    },
    {
        "name": "calculate_risk_profile",
        "description": "Calculates user's risk profile based on age, dependents, debt, and emergency fund",
        "input_schema": {
            "type": "object",
            "properties": {
                "age": {"type": "number"}
            },
            "required": ["age"]
        }
    },
    {
        "name": "calculate_emergency_fund",
        "description": "Checks if user has adequate emergency fund and calculates the gap",
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_expenses": {"type": "number"}
            },
            "required": ["monthly_expenses"]
        }
    },
    {
        "name": "calculate_net_worth",
        "description": "Calculates total assets minus liabilities and net worth health",
        "input_schema": {
            "type": "object",
            "properties": {
                "include_illiquid": {"type": "boolean"}
            },
            "required": ["include_illiquid"]
        }
    },
    {
        "name": "calculate_health_score",
        "description": "Calculates overall financial health score from 0-100 with grade",
        "input_schema": {
            "type": "object",
            "properties": {
                "detailed": {"type": "boolean"}
            },
            "required": ["detailed"]
        }
    },
    {
        "name": "allocate_surplus",
        "description": "Allocates surplus across emergency fund, debt, tax saving, and wealth building",
        "input_schema": {
            "type": "object",
            "properties": {
                "surplus": {"type": "number"}
            },
            "required": ["surplus"]
        }
    }
]

def fiduciary_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_surplus":
        result = calculate_investable_surplus(user)
        return f"Monthly surplus: ₹{result}"
    
    elif tool_name == "check_debt_priority":
        if not user.existing_debts:
            return "No debts found."
        highest_debt = max(user.existing_debts, key=lambda d: d.interest_rate)
        result = should_clear_debt(highest_debt)
        return f"Should clear debt first: {result}. Highest rate: {highest_debt.interest_rate}% on {highest_debt.debt_type}"
    
    elif tool_name == "calculate_risk_profile":
        result = calculate_risk_profile(user)
        return f"Risk Profile: {result['risk_profile']} (Score: {result['risk_score']}/100). {result['description']}"
    
    elif tool_name == "calculate_emergency_fund":
        result = calculate_emergency_fund(user)
        return f"Emergency Fund: {result['status']}. {result['months_covered']} months covered. Gap: ₹{result['gap']}. {result['message']}"
    
    elif tool_name == "calculate_net_worth":
        result = calculate_net_worth(user)
        return f"Net Worth: ₹{result['net_worth']}. Status: {result['net_worth_health']}. Assets: ₹{result['total_assets']}. Liabilities: ₹{result['total_liabilities']}"
    
    elif tool_name == "calculate_health_score":
        result = calculate_financial_health_score(user)
        breakdown = " | ".join([
            f"{k}: {v['score']}/{v['max']}"
            for k, v in result['breakdown'].items()
        ])
        return f"Health Score: {result['total_score']}/100 ({result['grade']} - {result['status']}). Breakdown: {breakdown}"
    
    elif tool_name == "allocate_surplus":
        surplus = calculate_investable_surplus(user)
        result = allocate_surplus(user, surplus)
        if result['status'] == 'NO_SURPLUS':
            return "No surplus available for allocation."
        allocations = " | ".join([
            f"{k}: ₹{v}" for k, v in result['allocations'].items()
        ])
        return f"Surplus Allocation: {allocations}"
    
    return "Tool not found"

def react_fiduciary_agent(state: VaultState) -> VaultState:
    from calculators.investable_surplus import calculate_investable_surplus
    from calculators.debt_priority import should_clear_debt
    
    user = state["user"]
    
    # Calculate deterministic truth first
    surplus = calculate_investable_surplus(user)
    
    highest_debt = max(user.existing_debts, key=lambda d: d.interest_rate) if user.existing_debts else None
    debt_priority = {
        "should_clear_debt": should_clear_debt(highest_debt) if highest_debt else False,
        "highest_rate": highest_debt.interest_rate if highest_debt else 0,
        "highest_debt_type": highest_debt.debt_type if highest_debt else None
    }
    
    if surplus < 0:
        financial_health = "EMERGENCY"
    elif debt_priority["should_clear_debt"]:
        financial_health = "CAUTION"
    else:
        financial_health = "HEALTHY"

    risk = calculate_risk_profile(user)
    emergency = calculate_emergency_fund(user)
    nw = calculate_net_worth(user)
    health = calculate_financial_health_score(user)
    goal_alloc = allocate_surplus(user, surplus)
    
    # Now get LLM verdict
    response, core_directive, team_brief = react_engine(
        user=user,
        persona=FIDUCIARY_PERSONA,
        tools=FIDUCIARY_TOOLS,
        tool_executor=fiduciary_executor,
        user_query=state.get("user_query", "Assess my complete financial situation."),
        state=state
    )
    
    return {
        "investable_surplus": surplus,
        "debt_priority": debt_priority,
        "financial_health": financial_health,
        "risk_assessment": risk,
        "emergency_fund_status": emergency,
        "net_worth_data": nw,
        "health_score": health,
        "goal_allocation": goal_alloc,
        "logic_anchor": core_directive,
        "agent_memos": {"Chief Fiduciary": response},
        "team_awareness": {"Chief Fiduciary": team_brief}
    }