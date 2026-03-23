from schemas.user_profile import UserFinancialProfile
from calculators.sip_allocator import calculate_required_sip
from calculators.investable_surplus import calculate_investable_surplus
from agents.react_engine import react_engine
from schemas.states import VaultState

SIP_PERSONA = """You are Priya Mehta — Investment Advisor.
You are speaking in a group chat. The Chief Fiduciary has already spoken and set the direction.

IDENTITY:
You are enthusiastic, coach-like, and genuinely excited about wealth building.
You make investing feel achievable and exciting, not scary or complex.
You address the user directly by name. You speak like their personal wealth coach.

RESEARCH RULE:
Always use search_investment_regulations to verify current SEBI approved fund categories and AMFI data.
Never recommend specific NAVs from memory.
REASONING RULE:
If no specific calculator exists for the user's question:
1. Use available calculators creatively to get relevant numbers
2. Use search tools to get current rates and data
3. Reason with those numbers to give a precise answer
Never say "I don't have a tool for that."
Always find a way to give a number-backed answer.

ADAPTIVE RESPONSE RULE:
- Full analysis → complete investment picture, fund allocation, growth projection
- Specific question → direct fund name, exact amount, what it builds
- Casual question → enthusiastic but grounded response

GROUP CHAT RULES:
1. RELEVANCE: If query is entirely about debt clearance or insurance with zero investment angle → output exactly: SKIP
2. THE ANCHOR (PREVIEW RULE): Read CORE_DIRECTIVE silently. If investments blocked — OBEY completely. Give one motivating preview of future wealth. Never say "I agree with Ramesh."
3. TEAM AWARENESS: Read TEAM_BRIEFs. If Tax Optimizer mentioned 80C gap — suggest ELSS immediately.

ANTI-REPETITION RULE:
Never open with validation.
Open with YOUR investment insight or the preview directly.

PROACTIVE ADVICE:
Always suggest Step-up SIP (10% annual increase).
Show what SIP builds in 10 and 25 years.
If 80C gap exists — ELSS solves investment AND tax together.

INVESTMENT RULES:
- < 3 years → Liquid/Debt funds
- 3-7 years → Balanced Advantage funds
- > 7 years → Pure Equity Index / Flexi Cap
- NEVER recommend when debt > 12% exists
- Only SEBI registered Indian funds

RESPONSE FORMAT:
Natural paragraphs. Enthusiastic but precise. Show future wealth always.
No headers. No templates.

TEAM_BRIEF FORMAT (MANDATORY — hidden from user):
TEAM_BRIEF: STATUS: [EMERGENCY/CAUTION/HEALTHY] | PLAN: [your recommendation within 20 words] | BLOCKED: [what you blocked] | KEY_NUMBER: [most critical figure]

LANGUAGE: English. Enthusiastic. Coach-like. Numbers with excitement.use hindi when you want to connect with th User."""

INVESTMENT_TOOLS = [
    {
        "name": "calculate_required_sip",
        "description": "Calculates monthly SIP needed to reach retirement corpus",
        "input_schema": {
            "type": "object",
            "properties": {
                "corpus_needed": {"type": "number"},
                "years_to_retirement": {"type": "number"}
            },
            "required": ["corpus_needed", "years_to_retirement"]
        }
    },
    {
        "name": "calculate_surplus",
        "description": "Calculates current investable surplus",
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_income": {"type": "number"}
            },
            "required": ["monthly_income"]
        }
    },
    {
    "name": "search_investment_regulations",
    "description": "Search current SEBI regulations, AMFI fund data, and mutual fund guidelines",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"]
    }
},
{
    "name": "calculate_stepup_sip",
    "description": "Shows how step-up SIP builds more wealth than flat SIP",
    "input_schema": {
        "type": "object",
        "properties": {
            "initial_monthly_sip": {"type": "number"},
            "annual_stepup_percent": {"type": "number"},
            "years": {"type": "number"}
        },
        "required": ["initial_monthly_sip", "annual_stepup_percent", "years"]
    }
},
{
    "name": "calculate_lumpsum_vs_sip",
    "description": "Compares lumpsum investment vs STP strategy for a windfall amount",
    "input_schema": {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
            "years": {"type": "number"}
        },
        "required": ["amount", "years"]
    }
},
{
    "name": "calculate_asset_allocation",
    "description": "Recommends optimal equity/debt/gold split based on age and risk profile",
    "input_schema": {
        "type": "object",
        "properties": {
            "investment_horizon_years": {"type": "number"}
        },
        "required": ["investment_horizon_years"]
    }
},
{
    "name": "calculate_market_timing_cost",
    "description": "Shows rupee cost of waiting for market crash instead of investing now",
    "input_schema": {
        "type": "object",
        "properties": {
            "monthly_sip": {"type": "number"},
            "months_waiting": {"type": "number"}
        },
        "required": ["monthly_sip", "months_waiting"]
    }
}
]

def investment_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_required_sip":
        corpus = tool_input.get("corpus_needed")
        years = tool_input.get("years_to_retirement")
        result = calculate_required_sip(corpus_needed=corpus, years_to_retirement=int(years))
        return f"Required SIP calculation: {result}"
    elif tool_name == "calculate_surplus":
        result = calculate_investable_surplus(user)
        return f"Current surplus: ₹{result}"
    elif tool_name == "search_investment_regulations":
        from tools.search_tool import search_domain
        query = tool_input.get("query")
        return search_domain(query, "sip")
    elif tool_name == "calculate_stepup_sip":
        from calculators.stepup_sip import calculate_stepup_sip
        result = calculate_stepup_sip(
            initial_monthly_sip=tool_input.get("initial_monthly_sip"),
            annual_stepup_percent=tool_input.get("annual_stepup_percent", 10),
            years=int(tool_input.get("years", 20))
        )
        return f"Step-up SIP analysis: {result}"

    elif tool_name == "calculate_lumpsum_vs_sip":
        from calculators.lumpsum_vs_sip import calculate_lumpsum_vs_sip
        result = calculate_lumpsum_vs_sip(
            amount=tool_input.get("amount"),
            years=int(tool_input.get("years", 10))
        )
        return f"Lumpsum vs STP analysis: {result}"

    elif tool_name == "calculate_asset_allocation":
        from calculators.asset_allocation import calculate_asset_allocation
        result = calculate_asset_allocation(
            age=user.age,
            risk_profile=user.risk_profile or "MODERATE",
            investment_horizon_years=int(tool_input.get("investment_horizon_years", 10)),
            monthly_surplus=calculate_investable_surplus(user)
        )
        return f"Asset allocation: {result}"

    elif tool_name == "calculate_market_timing_cost":
        from calculators.market_timing_cost import calculate_market_timing_cost
        result = calculate_market_timing_cost(
            monthly_sip=tool_input.get("monthly_sip"),
            months_waiting=int(tool_input.get("months_waiting", 6))
        )
        return f"Market timing cost: {result}"
    return "Tool not found"

def react_investment_agent(state: VaultState) -> VaultState:
    response, core_directive, team_brief = react_engine(
        user=state["user"],
        persona=SIP_PERSONA,
        tools=INVESTMENT_TOOLS,
        tool_executor=investment_executor,
        user_query=state.get("user_query", "Calculate my required SIP and investment plan."),
        state=state
    )
    if response.strip() == "SKIP":
        return {}
    return {
        "agent_memos": {"Investment Advisor": response},
        "team_awareness": {"Investment Advisor": team_brief}
    }