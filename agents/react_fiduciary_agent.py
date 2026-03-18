from schemas.user_profile import UserFinancialProfile
from calculators.investable_surplus import calculate_investable_surplus
from calculators.debt_priority import should_clear_debt
from agents.react_engine import react_engine
from schemas.states import VaultState

FIDUCIARY_PERSONA = """You are CA Ramesh Iyer — Senior Chartered Accountant with 25 years protecting Indian families.
You are the gatekeeper. Your job is to assess the complete financial picture and block harmful decisions.
You MUST use calculator tools before giving any verdict.
You speak directly. You use Hindi-English mix when being serious.
FIDUCIARY RULES:
- If surplus is negative → flag as financial emergency
- If any debt interest rate > 12% → block all investments
- If insurance critical gap exists → flag as urgent
- User cannot override your block without seeing the exact rupee cost
Maximum 4 bullet points. Always give a clear VERDICT at the top."""

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
    }
]

def fiduciary_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_surplus":
        result = calculate_investable_surplus(user)
        return f"Monthly surplus: ₹{result}"
    elif tool_name == "check_debt_priority":
        highest_debt = max(user.existing_debts, key=lambda d: d.interest_rate)
        result = should_clear_debt(highest_debt)
        return f"Should clear debt first: {result}. Highest rate: {highest_debt.interest_rate}%"
    return "Tool not found"

def react_fiduciary_agent(state: VaultState) -> VaultState:
    memo = react_engine(
        user=state["user"],
        persona=FIDUCIARY_PERSONA,
        tools=FIDUCIARY_TOOLS,
        tool_executor=fiduciary_executor,
        user_query="Analyze my debt situation and give me an action plan.",
        state=state
    )
    return {"agent_memos": {"fiduciary": memo}}