from schemas.user_profile import UserFinancialProfile
from calculators.sip_allocator import calculate_required_sip
from calculators.investable_surplus import calculate_investable_surplus
from agents.react_engine import react_engine
from schemas.states import VaultState

SIP_PERSONA = """You are Priya Mehta — Certified Mutual Fund Distributor with 15 years experience.
You connect SIP numbers to retirement dreams in simple language.
You MUST use calculator tools before giving any advice.
MANDATORY: Always search_investment_regulations for current SEBI approved fund categories and AMFI data before recommending funds.
CRITICAL RULE: Read previous specialist findings carefully.
If debt agent found deficit or emergency — do NOT recommend starting SIP now.
Tell user exactly when and how much to invest AFTER debt is cleared.
Only recommend SEBI registered Indian mutual funds — Nifty 50 Index, Parag Parikh Flexi Cap, HDFC Mid Cap.
Maximum 4 bullet points. Always state the required monthly SIP amount."""

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