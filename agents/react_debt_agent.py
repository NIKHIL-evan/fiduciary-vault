from schemas.user_profile import UserFinancialProfile
from calculators.investable_surplus import calculate_investable_surplus
from calculators.debt_priority import should_clear_debt
from calculators.debt_avalanche import calculate_avalanche_payment
from agents.react_engine import react_engine
from schemas.states import VaultState

DEBT_PERSONA = """You are Arjun Kapoor — Debt Strategist.
You are speaking in a group chat. The Chief Fiduciary has already spoken and set the direction.

IDENTITY:
You are aggressive, no-nonsense, and treat high-interest debt like an enemy to be destroyed.
You use war metaphors. You speak like a battle-hardened strategist who has seen debt destroy families.
You address the user directly by name. You never soften bad news.

RESEARCH RULE:
Use search_debt_regulations to verify current RBI repo rates and lending rates before advising.
Never quote rates from memory.
REASONING RULE:
If no specific calculator exists for the user's question:
1. Use available calculators creatively to get relevant numbers
2. Use search tools to get current rates and data
3. Reason with those numbers to give a precise answer
Never say "I don't have a tool for that."
Always find a way to give a number-backed answer.

ADAPTIVE RESPONSE RULE:
- Full analysis → war plan with exact steps, amounts, timeline
- Specific question → direct tactical answer, one number, one action
- Casual question → sharp, punchy response

GROUP CHAT RULES:
1. RELEVANCE: If user has NO debt and query is about tax or insurance → output exactly: SKIP
2. THE ANCHOR: Read CORE_DIRECTIVE silently. Act on it. Never say "I agree with Ramesh."
   Open with YOUR insight directly.
3. TEAM AWARENESS: Read TEAM_BRIEFs. Never repeat what others said.

ANTI-REPETITION RULE:
Never open with validation of another specialist.
Your first line must be YOUR aggressive debt insight.

PROACTIVE ADVICE:
Find balance transfer opportunities. Suggest pausing SIPs for 14%+ loans.
Show the rupee cost of minimum payment trap. Make debt feel like the enemy it is.

DEBT RULES:
- >30% → EMERGENCY. Destroy immediately.
- 12-30% → HIGH PRIORITY. No investments until cleared.
- <12% → LOW PRIORITY. Factor tax benefits before prepayment.

RESPONSE FORMAT:
Natural paragraphs. War metaphors welcome. Exact numbers always.
No headers. No templates.

TEAM_BRIEF FORMAT (MANDATORY — hidden from user):
TEAM_BRIEF: STATUS: [EMERGENCY/CAUTION/HEALTHY] | PLAN: [your recommendation within 20 words] | BLOCKED: [what you blocked] | KEY_NUMBER: [most critical figure]

LANGUAGE: English. Aggressive. Precise. War-like.Use Hindi when you want to connect with the user."""

DEBT_TOOLS = [
    {
        "name": "calculate_surplus",
        "description": "Calculates monthly investable surplus after expenses and debt payments",
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
        "description": "Checks if user should clear debt before investing",
        "input_schema": {
            "type": "object",
            "properties": {
                "interest_rate": {"type": "number"}
            },
            "required": ["interest_rate"]
        }
    },
    {
        "name": "calculate_avalanche",
        "description": "Finds which debt to pay first using avalanche method",
        "input_schema": {
            "type": "object",
            "properties": {
                "surplus": {"type": "number"}
            },
            "required": ["surplus"]
        }
    },
    {
    "name": "search_debt_regulations",
    "description": "Search current RBI repo rates, lending rates, and debt restructuring guidelines",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"]
    }
},
{
    "name": "calculate_balance_transfer",
    "description": "Calculates if transferring high-interest debt to lower rate saves money",
    "input_schema": {
        "type": "object",
        "properties": {
            "current_rate": {"type": "number"},
            "new_rate": {"type": "number"},
            "balance": {"type": "number"}
        },
        "required": ["current_rate", "new_rate", "balance"]
    }
},
{
    "name": "calculate_prepayment_benefit",
    "description": "Shows interest saved and years reduced by paying extra on a loan",
    "input_schema": {
        "type": "object",
        "properties": {
            "extra_monthly_payment": {"type": "number"},
            "debt_type": {"type": "string"}
        },
        "required": ["extra_monthly_payment", "debt_type"]
    }
},
{
    "name": "calculate_cheapest_capital",
    "description": "Finds cheapest way to raise emergency funds — LAMF vs gold loan vs FD vs selling MF",
    "input_schema": {
        "type": "object",
        "properties": {
            "amount_needed": {"type": "number"}
        },
        "required": ["amount_needed"]
    }
},
{
    "name": "calculate_debt_vs_investment",
    "description": "Compares if prepaying loan gives better returns than investing the same money",
    "input_schema": {
        "type": "object",
        "properties": {
            "loan_rate": {"type": "number"},
            "investment_return": {"type": "number"}
        },
        "required": ["loan_rate", "investment_return"]
    }
}
]

def debt_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_surplus":
        result = calculate_investable_surplus(user)
        return f"Investable surplus: ₹{result}"
    elif tool_name == "check_debt_priority":
        highest_debt = max(user.existing_debts, key=lambda d: d.interest_rate)
        result = should_clear_debt(highest_debt)
        return f"Should clear debt first: {result}. Highest rate: {highest_debt.interest_rate}%"
    elif tool_name == "calculate_avalanche":
        surplus = calculate_investable_surplus(user)
        result = calculate_avalanche_payment(user.existing_debts, surplus)
        return f"Avalanche plan: {result}"
    elif tool_name == "search_debt_regulations":
        from tools.search_tool import search_domain
        query = tool_input.get("query")
        return search_domain(query, "debt")
    elif tool_name == "calculate_balance_transfer":
        from calculators.balance_transfer import calculate_balance_transfer_benefit
        current_rate = tool_input.get("current_rate")
        new_rate = tool_input.get("new_rate")
        balance = tool_input.get("balance")
        highest_debt = max(user.existing_debts, key=lambda d: d.interest_rate)
        result = calculate_balance_transfer_benefit(
            current_balance=balance or highest_debt.amount,
            current_rate=current_rate or highest_debt.interest_rate,
            new_rate=new_rate
        )
        return f"Balance transfer analysis: {result}"

    elif tool_name == "calculate_prepayment_benefit":
        from calculators.prepayment_benefit import calculate_prepayment_benefit
        extra = tool_input.get("extra_monthly_payment")
        debt_type = tool_input.get("debt_type", "home_loan")
        target = next((d for d in user.existing_debts if debt_type in d.debt_type), None)
        if not target:
            target = min(user.existing_debts, key=lambda d: d.interest_rate)
        result = calculate_prepayment_benefit(
            principal=target.amount,
            annual_rate=target.interest_rate,
            tenure_years=20,
            extra_monthly_payment=extra
        )
        return f"Prepayment benefit: {result}"

    elif tool_name == "calculate_cheapest_capital":
        from calculators.cheapest_capital import calculate_cheapest_capital
        amount = tool_input.get("amount_needed")
        mf_value = sum(i.annual_amount for i in user.existing_investments)
        gold_value = sum(
            a.estimated_value for a in user.illiquid_assets
            if a.asset_type.lower() == "gold"
        )
        result = calculate_cheapest_capital(
            amount_needed=amount,
            mf_portfolio_value=mf_value,
            gold_value=gold_value
        )
        return f"Cheapest capital options: {result}"

    elif tool_name == "calculate_debt_vs_investment":
        from calculators.debt_vs_investment import calculate_debt_vs_investment
        result = calculate_debt_vs_investment(
            loan_amount=sum(d.amount for d in user.existing_debts),
            loan_rate=tool_input.get("loan_rate"),
            investment_return=tool_input.get("investment_return"),
            tax_bracket=30,
            is_home_loan=any(d.debt_type == "home_loan" for d in user.existing_debts),
            home_loan_interest_paid=sum(
                d.amount * d.interest_rate / 100
                for d in user.existing_debts
                if d.debt_type == "home_loan"
            )
        )
        return f"Debt vs investment analysis: {result}"
    return "Tool not found"

def react_debt_agent(state: VaultState) -> VaultState:
    response, core_directive, team_brief = react_engine(
        user=state["user"],
        persona=DEBT_PERSONA,
        tools=DEBT_TOOLS,
        tool_executor=debt_executor,
        user_query=state.get("user_query", "Analyze my debt situation and give me an action plan."),
        state=state
    )
    if response.strip() == "SKIP":
        return {}
    return {
        "agent_memos": {"Debt Strategist": response},
        "team_awareness": {"Debt Strategist": team_brief}
    }