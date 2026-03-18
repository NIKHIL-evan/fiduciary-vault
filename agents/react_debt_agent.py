from schemas.user_profile import UserFinancialProfile
from calculators.investable_surplus import calculate_investable_surplus
from calculators.debt_priority import should_clear_debt
from calculators.debt_avalanche import calculate_avalanche_payment
from agents.react_engine import react_engine
from schemas.states import VaultState

DEBT_PERSONA = """You are Arjun Kapoor — Debt Management Specialist.
You treat high-interest debt as a financial emergency.
You MUST use calculator tools before giving any advice.
Never guess numbers. Always calculate first, then reason.
Be aggressive and direct. Maximum 4 bullet points."""

DEBT_TOOLS = [
    {
        "name": "calculate_surplus",
        "description": "Calculates monthly investable surplus after expenses and debt payments",
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
        "description": "Checks if user should clear debt before investing",
        "input_schema": {
            "type": "object",
            "properties": {
                "interest_rate": {"type": "number"}
            },
            "required": ["interest_rate"]
        }
    },
    {
        "name": "calculate_avalanche",
        "description": "Finds which debt to pay first using avalanche method",
        "input_schema": {
            "type": "object",
            "properties": {
                "surplus": {"type": "number"}
            },
            "required": ["surplus"]
        }
    }
]

def debt_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_surplus":
        result = calculate_investable_surplus(user)
        return f"Investable surplus: ₹{result}"
    elif tool_name == "check_debt_priority":
        highest_debt = max(user.existing_debts, key=lambda d: d.interest_rate)
        result = should_clear_debt(highest_debt)
        return f"Should clear debt first: {result}. Highest rate: {highest_debt.interest_rate}%"
    elif tool_name == "calculate_avalanche":
        surplus = calculate_investable_surplus(user)
        result = calculate_avalanche_payment(user.existing_debts, surplus)
        return f"Avalanche plan: {result}"
    return "Tool not found"

def react_debt_agent(state: VaultState) -> VaultState:
    memo = react_engine(
        user=state["user"],
        persona=DEBT_PERSONA,
        tools=DEBT_TOOLS,
        tool_executor=debt_executor,
        user_query= "Analyze my debt situation and give me an action plan.",
        state=state
    )
    return {"agent_memos": {"debt": memo}}