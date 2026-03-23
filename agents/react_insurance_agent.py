from schemas.user_profile import UserFinancialProfile
from calculators.insurance_gap import calculate_insurance_gap
from agents.react_engine import react_engine
from schemas.states import VaultState

INSURANCE_PERSONA = """You are Vikram Singh — Risk Analyst.
You are speaking in a group chat. The Chief Fiduciary has already spoken and set the direction.

IDENTITY:
You are clinical, methodical, and see financial risk the way a doctor sees disease.
You quantify every gap in exact rupees. You speak with calm urgency — no panic, but no false comfort either.
You address the user directly by name.

RESEARCH RULE:
Always use search_insurance_regulations to verify current IRDAI requirements and premium estimates.
Never quote premium amounts from memory.
REASONING RULE:
If no specific calculator exists for the user's question:
1. Use available calculators creatively to get relevant numbers
2. Use search tools to get current rates and data
3. Reason with those numbers to give a precise answer
Never say "I don't have a tool for that."
Always find a way to give a number-backed answer.

ADAPTIVE RESPONSE RULE:
- Full analysis → complete risk picture, all gaps in rupees, clear priority
- Specific question → gap amount, product type, estimated premium
- Casual question → calm clinical response, one key risk number

GROUP CHAT RULES:
1. RELEVANCE: If query is strictly about stock picking or tax slabs with zero risk implications → output exactly: SKIP
2. THE ANCHOR: Read CORE_DIRECTIVE silently. CRITICAL EXCEPTION — basic protection cannot wait even during debt emergency. State this clinically, not defensively. Never say "I agree with Ramesh."
3. TEAM AWARENESS: Read TEAM_BRIEFs. Never repeat surplus numbers already stated.

ANTI-REPETITION RULE:
Never open with validation.
Open directly with the most critical risk you identified.

PROACTIVE ADVICE:
If dependents exist — flag term life gap first, always.
Employer insurance = ₹0 for planning. Always mention this.
ULIPs and endowments = flag immediately for surrender.

INSURANCE RULES:
- Health minimum: ₹10L individual, ₹20L family floater
- Term minimum: 15x annual income + total outstanding debt
- Dependents + zero term = SEVERE EMERGENCY. First line must say this.

RESPONSE FORMAT:
Natural paragraphs. Clinical tone. Gaps in exact rupees.
No headers. No templates.

TEAM_BRIEF FORMAT (MANDATORY — hidden from user):
TEAM_BRIEF: STATUS: [EMERGENCY/CAUTION/HEALTHY] | PLAN: [your recommendation within 20 words] | BLOCKED: [what you blocked] | KEY_NUMBER: [most critical figure]

LANGUAGE: English. Clinical. Calm. Precise.Use Hindi when you want to connect with the User"""

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
},
{
    "name": "calculate_surrender_benefit",
    "description": "Analyzes if surrendering existing LIC/ULIP/endowment policy is beneficial",
    "input_schema": {
        "type": "object",
        "properties": {
            "policy_type": {"type": "string"},
            "annual_premium": {"type": "number"},
            "surrender_value": {"type": "number"},
            "years_to_maturity": {"type": "number"},
            "maturity_value": {"type": "number"}
        },
        "required": ["policy_type", "annual_premium", "surrender_value", "years_to_maturity", "maturity_value"]
    }
},
{
    "name": "estimate_insurance_premium",
    "description": "Estimates annual premium for term life or health insurance based on age and cover",
    "input_schema": {
        "type": "object",
        "properties": {
            "cover_amount": {"type": "number"},
            "policy_type": {"type": "string"}
        },
        "required": ["cover_amount", "policy_type"]
    }
}
]

def insurance_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_insurance_gap":
        result = calculate_insurance_gap(
        monthly_income=user.monthly_income,
        term_insurance_cover=user.term_insurance_cover,
        health_insurance_cover=user.health_insurance_cover,
        has_dependents=any(m.is_dependent for m in user.family_members)
    )
        return f"Insurance gap analysis: {result}"
    elif tool_name == "search_insurance_regulations":
        from tools.search_tool import search_domain
        query = tool_input.get("query")
        return search_domain(query, "insurance")
    
    elif tool_name == "calculate_surrender_benefit":
        from calculators.surrender_value import calculate_surrender_benefit
        if not user.existing_policies:
            return "No existing policies found in profile."
        policy = user.existing_policies[0]
        result = calculate_surrender_benefit(
            policy_type=tool_input.get("policy_type", policy.policy_type),
            annual_premium=tool_input.get("annual_premium", policy.annual_premium),
            years_paid=1,
            surrender_value=tool_input.get("surrender_value", policy.surrender_value),
            maturity_value=tool_input.get("maturity_value", policy.coverage_amount),
            years_to_maturity=int(tool_input.get("years_to_maturity", policy.maturity_year - 2026))
        )
        return f"Surrender analysis: {result}"

    elif tool_name == "estimate_insurance_premium":
        from calculators.premium_estimator import estimate_insurance_premium
        result = estimate_insurance_premium(
            cover_amount=tool_input.get("cover_amount"),
            age=user.age,
            policy_type=tool_input.get("policy_type", "term"),
            family_size=len([m for m in user.family_members if m.is_dependent]) + 1
        )
        return f"Premium estimate: {result}"
    return "Tool not found"

def react_insurance_agent(state: VaultState) -> VaultState:
    response, core_directive, team_brief = react_engine(
        user=state["user"],
        persona=INSURANCE_PERSONA,
        tools=INSURANCE_TOOLS,
        tool_executor=insurance_executor,
        user_query=state.get("user_query", "Analyze my insurance coverage and identify critical gaps."),
        state=state
    )
    if response.strip() == "SKIP":
        return {}
    return {
        "agent_memos": {"Risk Analyst": response},
        "team_awareness": {"Risk Analyst": team_brief}
    }