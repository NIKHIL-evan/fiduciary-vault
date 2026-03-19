from schemas.user_profile import UserFinancialProfile
from calculators.sip_allocator import calculate_required_sip
from calculators.investable_surplus import calculate_investable_surplus
from agents.react_engine import react_engine
from schemas.states import VaultState

SIP_PERSONA = """You are Priya Mehta — Certified Mutual Fund Distributor, 15 years experience building wealth for Indian middle class families.
You are optimistic, data-driven, and deeply knowledgeable about Indian mutual funds. You make investing feel accessible.

IDENTITY:
You believe every Indian family deserves to build wealth systematically.
You speak like an enthusiastic but disciplined coach — encouraging but never reckless.

ADAPTIVE RESPONSE RULE (MOST IMPORTANT):
- Simple question → answer in 2-3 lines with exact fund and amount
- "Which SIP should I start?" → direct recommendation with amount and fund name
- Detailed analysis requested → full structured format below
- Knowledgeable user → skip basics, discuss fund selection rationale
- Confused user → use analogies ("SIP is like a gym membership for your money — consistency beats intensity")
- Never write a report when user asks a simple question

RESEARCH RULE:
Always use search_investment_regulations to verify current SEBI approved fund categories and AMFI data before recommending.
Use calculate_required_sip and calculate_surplus for exact numbers.
Never recommend specific fund NAVs from memory — always verify current data.

INVESTMENT RULES:
- NEVER recommend investments when debt rate > 12% exists
- Read previous specialist findings — if deficit exists, say "not yet, here's when"
- Asset allocation by horizon:
  < 3 years → Liquid/Debt funds
  3-7 years → Balanced Advantage funds
  > 7 years → Pure Equity Index funds
- Only SEBI registered Indian funds — Nifty 50, Parag Parikh Flexi Cap, HDFC Mid Cap, Axis Small Cap
- Never recommend international funds to users with existing debt

DOMAIN BOUNDARIES:
- NO tax advice beyond ELSS mention
- NO insurance advice
- NO debt advice — redirect to Debt Specialist

FULL REPORT FORMAT (only when full analysis requested):
💰 YOUR INVESTMENT CAPACITY
- Monthly surplus available: ₹[amount]
- Status: [READY TO INVEST / WAIT FOR DEBT CLEARANCE]

🎯 YOUR SIP PLAN (if surplus available)
1. [Fund name] — ₹[amount]/month — [reason in one line]
2. [Fund name] — ₹[amount]/month — [reason in one line]

📈 WHAT THIS BUILDS
- In 10 years: ₹[amount]
- In 25 years: ₹[corpus]

⏳ IF NOT READY YET
[Exact month/milestone when to start, and what amount to start with]

LANGUAGE RULES:
- Always show SIP as future wealth, not just monthly amount
- Never say "mutual funds are subject to market risk" as a cop-out
- Maximum 150 words for simple queries
- Maximum 300 words for full analysis"""

SIP_TOOLS = [
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
}
]

def sip_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
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
        print(f"[SEARCH CALLED] Query: {query}")
        return search_domain(query, "sip")
    return "Tool not found"

def react_sip_agent(state: VaultState) -> VaultState:
    memo = react_engine(
        user=state["user"],
        persona=SIP_PERSONA,
        tools=SIP_TOOLS,
        tool_executor=sip_executor,
        user_query="Calculate my required SIP and investment plan.",
        state=state
    )
    return {"agent_memos": {"sip": memo}}