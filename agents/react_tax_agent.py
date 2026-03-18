from schemas.user_profile import UserFinancialProfile
from calculators.tax_savings import calculate_tax_savings
from agents.react_engine import react_engine
from schemas.states import VaultState

TAX_PERSONA = """You are CA Priya Sharma — Chartered Accountant specializing in tax optimization.
Your clients pay for exact rupee savings, not vague guidance.
You MUST use calculator tools before giving any advice.
Never guess tax amounts. Always calculate first, then reason.
RULE: Only recommend SEBI registered Indian instruments — PPF, ELSS, NPS, NSC.
Maximum 4 bullet points. Always show exact rupee amount saved."""

TAX_TOOLS = [
    {
        "name": "calculate_tax_savings",
        "description": "Calculates 80C utilization, remaining limit, and potential tax saved",
        "input_schema": {
            "type": "object",
            "properties": {
                "tax_regime": {"type": "string"}
            },
            "required": ["tax_regime"]
        }
    }
]

def tax_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_tax_savings":
        result = calculate_tax_savings(
            annual_income=user.monthly_income * 12,
            existing_investments=user.existing_investments,
            tax_regime=user.tax_regime
        )
        return f"Tax calculation result: {result}"
    return "Tool not found"

def react_tax_agent(state: VaultState) -> VaultState:
    memo = react_engine(
        user=state["user"],
        persona=TAX_PERSONA,
        tools=TAX_TOOLS,
        tool_executor=tax_executor,
        user_query="Analyze my tax situation and tell me how to save maximum tax.",
        state=state
    )
    return {"agent_memos": {"tax": memo}}