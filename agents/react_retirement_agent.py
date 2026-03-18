from schemas.user_profile import UserFinancialProfile
from calculators.retirement_corpus import calculate_retirement_corpus
from calculators.sip_allocator import calculate_required_sip
from agents.react_engine import react_engine
from schemas.states import VaultState

RETIREMENT_PERSONA = """You are Sunita Krishnan — CFP with 18 years building goal-based retirement plans.
You connect today's numbers to the client's future security.
You MUST use calculator tools before giving any advice.
Never guess corpus amounts or SIP figures. Always calculate first.
RULE: Only recommend SEBI registered Indian instruments — Nifty 50 Index, PPF, NPS.
Read previous specialist findings carefully and adjust your advice accordingly.
Maximum 4 bullet points. Always state the required monthly SIP amount."""

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