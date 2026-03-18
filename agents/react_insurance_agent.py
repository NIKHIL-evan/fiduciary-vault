from schemas.user_profile import UserFinancialProfile
from calculators.insurance_gap import calculate_insurance_gap
from agents.react_engine import react_engine
from schemas.states import VaultState

INSURANCE_PERSONA = """You are Vikram Singh — IRDAI-licensed Risk Management Consultant.
You find holes in financial armor and quantify the exposure bluntly.
You MUST use calculator tools before giving any advice.
CRITICAL RULE: If dependents exist and term cover gap > 0, first line must be SEVERE EMERGENCY.
Read previous specialist findings and factor in surplus availability for premium recommendations.
Never recommend ULIPs or endowment plans. Term insurance only.
Maximum 4 bullet points."""

INSURANCE_TOOLS = [
    {
        "name": "calculate_insurance_gap",
        "description": "Calculates term life and health insurance gaps based on income and current coverage",
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_income": {"type": "number"},
                "has_dependents": {"type": "boolean"}
            },
            "required": ["monthly_income", "has_dependents"]
        }
    }
]

def insurance_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_insurance_gap":
        result = calculate_insurance_gap(
            monthly_income=user.monthly_income,
            term_insurance_cover=user.term_insurance_cover,
            health_insurance_cover=user.health_insurance_cover,
            has_dependents=len(user.dependents) > 0
        )
        return f"Insurance gap analysis: {result}"
    return "Tool not found"

def react_insurance_agent(state: VaultState) -> VaultState:
    memo = react_engine(
        user=state["user"],
        persona=INSURANCE_PERSONA,
        tools=INSURANCE_TOOLS,
        tool_executor=insurance_executor,
        user_query="Analyze my insurance coverage and identify critical gaps.",
        state=state
    )
    return {"agent_memos": {"insurance": memo}}