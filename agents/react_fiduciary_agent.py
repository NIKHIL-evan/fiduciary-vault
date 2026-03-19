from schemas.user_profile import UserFinancialProfile
from calculators.investable_surplus import calculate_investable_surplus
from calculators.debt_priority import should_clear_debt
from agents.react_engine import react_engine
from schemas.states import VaultState

FIDUCIARY_PERSONA = """You are CA Ramesh Iyer — Senior Chartered Accountant, 25 years experience, Mumbai.
You have seen thousands of Indian families make the same mistakes. You are a trusted family advisor, not a consultant.

IDENTITY:
You speak directly. You use Hindi-English mix when being serious. You never sugarcoat bad news.
You treat every client like your own family member — honest, caring, firm.

ADAPTIVE RESPONSE RULE (MOST IMPORTANT):
- Simple question → answer in 2-3 lines. No report. No headers.
- Detailed analysis requested → use full structured format below
- Knowledgeable user → skip basics, go deep into numbers
- Confused user → simplify everything, use analogies
- Always match your response depth to what the user actually asked
- A real CA doesn't write a 500-word report when someone asks "should I invest today?"

FIDUCIARY RULES (NON-NEGOTIABLE):
- Always use calculator tools before giving any verdict
- If surplus is negative → say it plainly, no softening
- If any debt rate > 12% → block investments, explain why in rupees
- Never recommend investments before debt is assessed
- Every number must have context — not just ₹10,500 but "that's more than your child's school fees gone every month"

RESEARCH RULE:
Always use calculator tools first for numbers.
If user asks about current regulations, interest rates, or government schemes — use search tools to verify before answering. Never quote rates from memory.

FULL REPORT FORMAT (only when full analysis is requested):
🚨 YOUR SITUATION
[One brutal honest sentence]

✅ DO THIS WEEK (max 3 actions)
1. [Action] → [Why, in rupees]
2. [Action] → [Why, in rupees]
3. [Action] → [Why, in rupees]

📅 NEXT 3-6 MONTHS
[2 points maximum]

⚠️ THE ONE THING THAT WILL DESTROY YOU IF IGNORED
[One specific warning with rupee impact]

LANGUAGE RULES:
- No jargon without explanation
- Hindi-English mix for serious moments
- Maximum 150 words for simple queries
- Maximum 300 words for full analysis"""

FIDUCIARY_TOOLS = [
    {
        "name": "calculate_surplus",
        "description": "Calculates monthly investable surplus after all expenses and debt payments",
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_income": {"type": "number"}
            },
            "required": ["monthly_income"]
        }
    },
    {
        "name": "check_debt_priority",
        "description": "Checks if any debt should be cleared before investing",
        "input_schema": {
            "type": "object",
            "properties": {
                "interest_rate": {"type": "number"}
            },
            "required": ["interest_rate"]
        }
    }
]

def fiduciary_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_surplus":
        result = calculate_investable_surplus(user)
        return f"Monthly surplus: ₹{result}"
    elif tool_name == "check_debt_priority":
        highest_debt = max(user.existing_debts, key=lambda d: d.interest_rate)
        result = should_clear_debt(highest_debt)
        return f"Should clear debt first: {result}. Highest rate: {highest_debt.interest_rate}%"
    return "Tool not found"

def react_fiduciary_agent(state: VaultState) -> VaultState:
    from calculators.investable_surplus import calculate_investable_surplus
    from calculators.debt_priority import should_clear_debt
    
    user = state["user"]
    
    # Calculate deterministic truth first
    surplus = calculate_investable_surplus(user)
    
    highest_debt = max(user.existing_debts, key=lambda d: d.interest_rate) if user.existing_debts else None
    debt_priority = {
        "should_clear_debt": should_clear_debt(highest_debt) if highest_debt else False,
        "highest_rate": highest_debt.interest_rate if highest_debt else 0,
        "highest_debt_type": highest_debt.debt_type if highest_debt else None
    }
    
    if surplus < 0:
        financial_health = "EMERGENCY"
    elif debt_priority["should_clear_debt"]:
        financial_health = "CAUTION"
    else:
        financial_health = "HEALTHY"
    
    # Now get LLM verdict
    memo = react_engine(
        user=user,
        persona=FIDUCIARY_PERSONA,
        tools=FIDUCIARY_TOOLS,
        tool_executor=fiduciary_executor,
        user_query="Assess my complete financial situation and give your verdict.",
        state=state
    )
    
    return {
        "investable_surplus": surplus,
        "debt_priority": debt_priority,
        "financial_health": financial_health,
        "agent_memos": {"fiduciary": memo}
    }