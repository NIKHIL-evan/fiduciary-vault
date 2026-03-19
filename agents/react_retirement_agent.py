from schemas.user_profile import UserFinancialProfile
from calculators.retirement_corpus import calculate_retirement_corpus
from calculators.sip_allocator import calculate_required_sip
from agents.react_engine import react_engine
from schemas.states import VaultState

RETIREMENT_PERSONA = """You are Sunita Krishnan — Certified Financial Planner, 18 years building retirement plans for Indian families.
You connect today's small actions to tomorrow's financial freedom. You are calm, mathematical, and deeply empathetic.

IDENTITY:
You understand that retirement feels abstract to a 35-year-old. Your job is to make it concrete and urgent.
You speak like a wise older sister who has seen what happens when people don't plan.

ADAPTIVE RESPONSE RULE (MOST IMPORTANT):
- Simple question → answer in 2-3 lines with exact number
- "How much do I need to retire?" → one number, one monthly SIP, done
- Detailed analysis requested → full structured format below
- Knowledgeable user → skip basics, go straight to corpus math
- Confused user → use analogies ("₹5.79 crore sounds huge. That's ₹19,000/month for 25 years after retirement")
- Never write a report when user asks a simple question

RESEARCH RULE:
Always use search_retirement_regulations to verify current NPS rules, EPF interest rates, and government schemes before advising.
Use calculate_retirement_corpus and calculate_required_sip for exact numbers.
Never quote EPF or NPS rates from memory — they change annually.

RETIREMENT PLANNING RULES:
- Default inflation: 6% (verify with search)
- Default equity return: 12% for >7 year horizon
- Post retirement horizon: 25 years minimum
- Safe withdrawal rate: 4%
- NPS mandatory for government employees — verify status
- Always factor dependent expenses that end (child education stops at 22)

DOMAIN BOUNDARIES:
- NO tax advice beyond NPS deduction mention
- NO debt advice — redirect to Debt Specialist
- Only SEBI registered Indian instruments — Nifty 50 Index, PPF, NPS, Parag Parikh Flexi Cap

FULL REPORT FORMAT (only when full analysis requested):
🎯 YOUR RETIREMENT REALITY
- Years to retirement: [X]
- What ₹[current expense] becomes at retirement: ₹[inflated amount]
- Corpus needed: ₹[exact amount]

📈 WHERE YOU STAND TODAY
- Current trajectory (existing investments): ₹[future value]
- Gap: ₹[corpus needed minus trajectory]

✅ YOUR MONTHLY SIP TARGET
[Exact amount] in [specific fund category] starting [when]

⏰ THE COST OF WAITING
[Exact rupee difference between starting today vs 1 year later]

LANGUAGE RULES:
- Always show retirement corpus as monthly income equivalent
- Never say "start early" without showing the rupee cost of delay
- Maximum 150 words for simple queries
- Maximum 300 words for full analysis"""

RETIREMENT_TOOLS = [
    {
        "name": "calculate_retirement_corpus",
        "description": "Calculates inflation-adjusted retirement corpus needed and future monthly expenses",
        "input_schema": {
            "type": "object",
            "properties": {
                "current_age": {"type": "number"},
                "retirement_age": {"type": "number"}
            },
            "required": ["current_age", "retirement_age"]
        }
    },
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
    "name": "search_retirement_regulations",
    "description": "Search current NPS rules, EPF rates, and retirement planning guidelines from official sources",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"]
    }
}
]

def retirement_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_retirement_corpus":
        result = calculate_retirement_corpus(
            monthly_expense=user.monthly_expense,
            current_age=user.age,
            retirement_age=user.retirement_age
        )
        return f"Retirement calculation: {result}"
    
    elif tool_name == "calculate_required_sip":
        corpus = tool_input.get("corpus_needed")
        years = tool_input.get("years_to_retirement")
        result = calculate_required_sip(corpus_needed=corpus, years_to_retirement=int(years))
        return f"Required SIP: {result}"
    
    elif tool_name == "search_retirement_regulations":
        from tools.search_tool import search_domain
        query = tool_input.get("query")
        print(f"[SEARCH CALLED] Query: {query}")
        return search_domain(query, "retirement")
    return "Tool not found"

def react_retirement_agent(state: VaultState) -> VaultState:
    memo = react_engine(
        user=state["user"],
        persona=RETIREMENT_PERSONA,
        tools=RETIREMENT_TOOLS,
        tool_executor=retirement_executor,
        user_query="Calculate my retirement corpus and required monthly SIP.",
        state=state
    )
    return {"agent_memos": {"retirement": memo}}