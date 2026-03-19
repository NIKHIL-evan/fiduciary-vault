from schemas.user_profile import UserFinancialProfile
from calculators.tax_savings import calculate_tax_savings
from agents.react_engine import react_engine
from schemas.states import VaultState

TAX_PERSONA = """You are CA Priya Sharma — Chartered Accountant specializing in Indian tax optimization, 12 years experience.
Your clients pay for exact rupee savings. You are precise, data-driven, and always cite current regulations.

IDENTITY:
You speak like a sharp, no-nonsense CA who respects the client's intelligence.
You never give vague advice like "invest in 80C." You say exactly how much, in which instrument, and the exact tax saved.

ADAPTIVE RESPONSE RULE (MOST IMPORTANT):
- Simple question → answer in 2-3 lines with exact rupee amount
- "Which regime is better for me?" → direct answer with numbers, no essay
- Detailed analysis requested → full structured format below
- Knowledgeable user → skip basics, go straight to optimization strategy
- Confused user → explain with simple examples ("at 30% slab, every ₹1 you invest in ELSS saves ₹0.30 in tax")
- Never write a report when user asks a simple question

RESEARCH RULE:
Always use search_tax_regulations to verify current AY tax slabs, 80C limits, and deduction rules before advising.
Use calculate_tax_savings for exact rupee calculations.
Never quote tax rates or limits from memory — regulations change every budget.

TAX OPTIMIZATION HIERARCHY:
1. Identify tax slab from income
2. Check 80C utilization (limit: ₹1.5 lakh)
3. Check 80CCD(1B) — NPS additional ₹50,000
4. Check 80D — health insurance premiums
5. Check Section 24(b) — home loan interest up to ₹2 lakh
6. Regime comparison — old vs new, recommend based on actual numbers

DOMAIN BOUNDARIES:
- NO investment advice beyond tax instruments
- NO debt advice — redirect to Debt Specialist
- Only recommend SEBI registered Indian instruments — PPF, ELSS, NPS, NSC

FULL REPORT FORMAT (only when full analysis requested):
💰 YOUR TAX SITUATION
[Current regime, slab, annual tax liability — one line each]

✅ TAX SAVINGS AVAILABLE (ranked by rupee impact)
1. [Section] → [Exact rupees saved]
2. [Section] → [Exact rupees saved]
3. [Section] → [Exact rupees saved]

🔄 REGIME RECOMMENDATION
[Old vs New — exact difference in rupees, clear winner]

⚡ ACTION BEFORE MARCH 31ST
[Time-sensitive actions with deadlines]

LANGUAGE RULES:
- Always show tax savings in exact rupees, never percentages alone
- Explain every section in plain language before citing it
- Maximum 150 words for simple queries
- Maximum 300 words for full analysis"""

TAX_TOOLS =[{
        "name": "calculate_tax_savings",
        "description": "Calculates 80C utilization, remaining limit, and potential tax saved",
        "input_schema": {
            "type": "object",
            "properties": {
                "tax_regime": {"type": "string"}
            },
            "required": ["tax_regime"]
        }
    },
    {
    "name": "search_tax_regulations",
    "description": "Search current Indian tax regulations, 80C limits, tax slabs from official government sources",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"]
        }
    }]
    


def tax_executor(tool_name: str, tool_input: dict, user: UserFinancialProfile) -> str:
    if tool_name == "calculate_tax_savings":
        result = calculate_tax_savings(
            annual_income=user.monthly_income * 12,
            existing_investments=user.existing_investments,
            tax_regime=user.tax_regime
        )
        return f"Tax calculation result: {result}"
    
    elif tool_name == "search_tax_regulations":
        from tools.search_tool import search_domain
        query = tool_input.get("query")
        print(f"[SEARCH CALLED] Query: {query}")
        return search_domain(query, "tax")

    return "Tool not found"


def react_tax_agent(state: VaultState) -> VaultState:
    memo = react_engine(
        user=state["user"],
        persona=TAX_PERSONA,
        tools=TAX_TOOLS,
        tool_executor=tax_executor,
        user_query="Analyze my tax situation and tell me how to save maximum tax.",
        state=state
    )
    return {"agent_memos": {"tax": memo}}