from schemas.user_profile import UserFinancialProfile
from calculators.retirement_corpus import calculate_retirement_corpus
from calculators.sip_allocator import calculate_required_sip
from agents.react_engine import react_engine
from schemas.states import VaultState

RETIREMENT_PERSONA = """You are Sunita Krishnan — Retirement Planner.
You are speaking in a group chat. The Chief Fiduciary has already spoken and set the direction.

IDENTITY:
You are warm, future-focused, and tell stories about what life looks like at 60.
You make numbers human. You connect today's struggle to tomorrow's freedom.
You address the user directly by name. You speak like someone who genuinely cares about their future.

RESEARCH RULE:
Always use search_retirement_regulations to verify current NPS rules and EPF interest rates.
Never quote rates from memory.
REASONING RULE:
If no specific calculator exists for the user's question:
1. Use available calculators creatively to get relevant numbers
2. Use search tools to get current rates and data
3. Reason with those numbers to give a precise answer
Never say "I don't have a tool for that."
Always find a way to give a number-backed answer.

ADAPTIVE RESPONSE RULE:
- Full analysis → paint the retirement picture, corpus, monthly income equivalent, SIP required
- Specific question → one number, what it means in real life
- Casual question → warm story-driven response

GROUP CHAT RULES:
1. RELEVANCE: If query is strictly about short-term debt or daily budgeting with zero long-term implications → output exactly: SKIP
2. THE ANCHOR: Read CORE_DIRECTIVE silently. If investments blocked, give the "Preview" — what retirement looks like once debt is cleared. Never say "I agree with Ramesh."
3. TEAM AWARENESS: Read TEAM_BRIEFs. If Investment Advisor mentioned SIP amount, align corpus with it.

ANTI-REPETITION RULE:
Never open with validation.
Open with a future-focused observation about their retirement reality.

PROACTIVE ADVICE:
Always show rupee cost of waiting 1 year.
Always translate corpus to monthly income ("₹5.79Cr = ₹48k/month for 25 years").
Factor dependent expenses that end — child education stops at 22.

RETIREMENT RULES:
- Default inflation: 6%
- Equity return: 12% for >7 years
- Safe withdrawal rate: 4%
- Post retirement: 25 years minimum
- Only SEBI registered: Nifty 50, PPF, NPS, Parag Parikh Flexi Cap

RESPONSE FORMAT:
Natural paragraphs. Warm storytelling tone. Bold key numbers.
No headers. No templates. One exact action at the end.

TEAM_BRIEF FORMAT (MANDATORY — hidden from user):
TEAM_BRIEF: STATUS: [EMERGENCY/CAUTION/HEALTHY] | PLAN: [your recommendation within 20 words] | BLOCKED: [what you blocked] | KEY_NUMBER: [most critical figure]

LANGUAGE: English. Warm. Story-driven. Future-focused. Use Hindi when you want to Connect with the user"""

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
},
{
    "name": "calculate_education_goal",
    "description": "Calculates SIP needed for child's education goal",
    "input_schema": {
        "type": "object",
        "properties": {
            "child_age": {"type": "number"},
            "current_cost": {"type": "number"}
        },
        "required": ["child_age", "current_cost"]
    }
},
{
    "name": "calculate_epf_future_value",
    "description": "Projects EPF corpus at retirement based on current balance and salary",
    "input_schema": {
        "type": "object",
        "properties": {
            "current_epf_balance": {"type": "number"}
        },
        "required": ["current_epf_balance"]
    }
},
{
    "name": "calculate_post_retirement_income",
    "description": "Calculates monthly income from EPF, PPF, NPS and rental after retirement",
    "input_schema": {
        "type": "object",
        "properties": {
            "epf_corpus": {"type": "number"},
            "ppf_corpus": {"type": "number"}
        },
        "required": ["epf_corpus", "ppf_corpus"]
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
        return search_domain(query, "retirement")
    elif tool_name == "calculate_education_goal":
        from calculators.education_goal import calculate_education_goal
        child_age = tool_input.get("child_age")
        if not child_age:
            children = [m for m in user.family_members if m.relation.lower() == "child"]
            child_age = children[0].age if children else 5
        result = calculate_education_goal(
            child_age=int(child_age),
            current_cost=tool_input.get("current_cost", 1500000)
        )
        return f"Education goal: {result}"

    elif tool_name == "calculate_epf_future_value":
        from calculators.epf_future_value import calculate_epf_future_value
        result = calculate_epf_future_value(
            current_epf_balance=tool_input.get("current_epf_balance", user.epf_balance),
            monthly_salary=user.monthly_income,
            current_age=user.age,
            retirement_age=user.retirement_age
        )
        return f"EPF future value: {result}"

    elif tool_name == "calculate_post_retirement_income":
        from calculators.post_retirement_income import calculate_post_retirement_income
        result = calculate_post_retirement_income(
            epf_corpus=tool_input.get("epf_corpus", 0),
            ppf_corpus=tool_input.get("ppf_corpus", 0),
            nps_corpus=0,
            rental_income_monthly=0
        )
        return f"Post retirement income: {result}"
    return "Tool not found"

def react_retirement_agent(state: VaultState) -> VaultState:
    response, core_directive, team_brief = react_engine(
        user=state["user"],
        persona=RETIREMENT_PERSONA,
        tools=RETIREMENT_TOOLS,
        tool_executor=retirement_executor,
        user_query=state.get("user_query", "Calculate my retirement corpus and required monthly SIP."),
        state=state
    )
    if response.strip() == "SKIP":
        return {}
    return {
        "agent_memos": {"Retirement Planner": response},
        "team_awareness": {"Retirement Planner": team_brief}
    }