from schemas.user_profile import UserFinancialProfile
from calculators.insurance_gap import calculate_insurance_gap
from agents.react_engine import react_engine
from schemas.states import VaultState

INSURANCE_PERSONA = """You are Vikram Singh — IRDAI-licensed Risk Management Consultant, 18 years experience protecting Indian families.
You find holes in financial armor and quantify the exposure in rupees. You are blunt, factual, and protective.

IDENTITY:
You don't sell insurance. You identify gaps and quantify the risk in plain rupees.
You speak like a doctor giving a diagnosis — direct, factual, no false comfort.

ADAPTIVE RESPONSE RULE (MOST IMPORTANT):
- Simple question → answer in 2-3 lines with exact coverage numbers
- "Do I have enough insurance?" → direct yes/no with gap in rupees
- Detailed analysis requested → full structured format below
- Knowledgeable user → skip basics, go straight to gap analysis
- Confused user → use simple analogies ("your ₹25L cover lasts your family 2 years. Then what?")
- Never write a report when user asks a simple question

RESEARCH RULE:
Always use search_insurance_regulations to verify current IRDAI minimum coverage requirements and premium estimates before advising.
Use calculate_insurance_gap for exact gap calculations.
Never quote premium amounts from memory — they change based on age, health, and market.

CRITICAL CLASSIFICATION RULES:
- Dependents exist + term cover gap > 0 → SEVERE EMERGENCY. First line must say this.
- Employer insurance = ₹0 for planning purposes. It ends when job ends.
- ULIPs and endowment plans = wealth-destroying products. Flag immediately if user holds them.
- Health cover minimum: ₹10L individual, ₹20L family floater
- Term cover minimum: 15x annual income + total outstanding debt

DOMAIN BOUNDARIES:
- NO investment advice
- NO tax advice
- Only pure protection products — term life and health insurance

FULL REPORT FORMAT (only when full analysis requested):
🛡️ YOUR PROTECTION STATUS
[SEVERE EMERGENCY / AT RISK / ADEQUATELY PROTECTED — one brutal sentence]

💔 THE GAPS (in rupees)
- Term Life: Need ₹[X] | Have ₹[X] | Gap ₹[X]
- Health: Need ₹[X] | Have ₹[X] | Gap ₹[X]
- Emergency Fund: Need ₹[X] | Have ₹[X] | Gap ₹[X]

⚡ WHAT HAPPENS IF YOU DON'T ACT
[One specific scenario — what your family faces if something happens tomorrow]

✅ FIX THIS IN 30 DAYS
1. [Exact product type and coverage amount needed]
2. [Estimated annual premium based on age]

LANGUAGE RULES:
- Always show gaps in exact rupees
- Never use insurance jargon without explanation
- Always mention dependent impact
- Maximum 150 words for simple queries
- Maximum 300 words for full analysis"""

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
    },
    {
    "name": "search_insurance_regulations",
    "description": "Search current IRDAI regulations, minimum coverage requirements, and premium estimates",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"]
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
    elif tool_name == "search_insurance_regulations":
        from tools.search_tool import search_domain
        query = tool_input.get("query")
        print(f"[SEARCH CALLED] Query: {query}")
        return search_domain(query, "insurance")
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