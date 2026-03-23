from schemas.user_profile import UserFinancialProfile
from calculators.tax_savings import calculate_tax_savings
from agents.react_engine import react_engine
from schemas.states import VaultState

TAX_PERSONA = """You are CA Priya Sharma — Tax Optimizer.
You are speaking in a group chat. The Chief Fiduciary has already spoken and set the direction.

IDENTITY:
You are precise, methodical, and numbers-first. Every rupee saved in tax is a victory.
You speak like a professional who has studied the tax code so the client doesn't have to.
You address the user directly by name. You never give vague advice.

RESEARCH RULE:
Always use search_tax_regulations to verify current AY tax slabs, 80C limits before advising.
Never quote tax rates from memory — regulations change every budget.
REASONING RULE:
If no specific calculator exists for the user's question:
1. Use available calculators creatively to get relevant numbers
2. Use search tools to get current rates and data
3. Reason with those numbers to give a precise answer
Never say "I don't have a tool for that."
Always find a way to give a number-backed answer.

ADAPTIVE RESPONSE RULE:
- Full analysis → complete tax picture, all sections, exact rupees saved
- Specific question → exact number, one section, done
- Casual question → clean professional answer, no jargon

GROUP CHAT RULES:
1. RELEVANCE: If query is strictly about debt clearance or car purchase with zero tax implications → output exactly: SKIP
2. THE ANCHOR: Read CORE_DIRECTIVE silently. Align tax strategy with financial health.
   Never say "As Ramesh said." Open with YOUR tax insight.
3. TEAM AWARENESS: Read TEAM_BRIEFs. If Investment Advisor mentioned ELSS, confirm the tax math.
   If Debt Strategist mentioned home loan, calculate Section 24(b) immediately.

ANTI-REPETITION RULE:
Never validate another specialist's point.
Open directly with your tax finding.

PROACTIVE ADVICE:
Hunt for every missed deduction. 80C, 80D, 80CCD(1B), Section 24(b).
Always compare old vs new regime with exact rupee difference.
Never leave money on the table.

TAX HIERARCHY:
1. Tax slab identification
2. 80C utilization (₹1.5L limit)
3. 80CCD(1B) NPS (₹50k additional)
4. 80D health insurance
5. Section 24(b) home loan interest
6. Regime comparison

DOMAIN: Only SEBI registered instruments — PPF, ELSS, NPS, NSC.

RESPONSE FORMAT:
Natural paragraphs. Exact rupees always. Professional tone.
No headers. No templates.

TEAM_BRIEF FORMAT (MANDATORY — hidden from user):
TEAM_BRIEF: STATUS: [EMERGENCY/CAUTION/HEALTHY] | PLAN: [your recommendation within 20 words] | BLOCKED: [what you blocked] | KEY_NUMBER: [most critical figure]

LANGUAGE: English. Precise. Professional. Numbers-first. Use Hindi When you want to connect to the user"""

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
    },
    {
    "name": "calculate_capital_gains_tax",
    "description": "Calculates LTCG or STCG tax on mutual fund or stock sale",
    "input_schema": {
        "type": "object",
        "properties": {
            "purchase_value": {"type": "number"},
            "sale_value": {"type": "number"},
            "holding_months": {"type": "number"},
            "asset_type": {"type": "string"}
        },
        "required": ["purchase_value", "sale_value", "holding_months", "asset_type"]
    }
},
{
    "name": "calculate_hra_exemption",
    "description": "Calculates HRA tax exemption based on rent paid and salary",
    "input_schema": {
        "type": "object",
        "properties": {
            "rent_paid_annual": {"type": "number"},
            "is_metro": {"type": "boolean"}
        },
        "required": ["rent_paid_annual", "is_metro"]
    }
},
{
    "name": "calculate_tax_harvesting",
    "description": "Finds tax saving opportunity by selling losing investments to offset gains",
    "input_schema": {
        "type": "object",
        "properties": {
            "total_gains": {"type": "number"},
            "total_losses": {"type": "number"}
        },
        "required": ["total_gains", "total_losses"]
    }
},
{
    "name": "calculate_family_tax_arbitrage",
    "description": "Calculates tax saved by gifting investments to low-bracket family member",
    "input_schema": {
        "type": "object",
        "properties": {
            "investment_amount": {"type": "number"},
            "investment_return_percent": {"type": "number"},
            "family_member_relation": {"type": "string"}
        },
        "required": ["investment_amount", "investment_return_percent", "family_member_relation"]
    }
},
{
    "name": "calculate_esop_tax",
    "description": "Calculates perquisite tax owed on ESOP/RSU vesting",
    "input_schema": {
        "type": "object",
        "properties": {
            "vesting_value": {"type": "number"},
            "purchase_price": {"type": "number"}
        },
        "required": ["vesting_value", "purchase_price"]
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
        return search_domain(query, "tax")
    
    elif tool_name == "calculate_capital_gains_tax":
        from calculators.ltcg_stcg import calculate_capital_gains_tax
        result = calculate_capital_gains_tax(
            purchase_value=tool_input.get("purchase_value"),
            sale_value=tool_input.get("sale_value"),
            holding_months=int(tool_input.get("holding_months")),
            asset_type=tool_input.get("asset_type", "equity"),
            tax_bracket=30
        )
        return f"Capital gains tax: {result}"

    elif tool_name == "calculate_hra_exemption":
        from calculators.hra_calculator import calculate_hra_exemption
        result = calculate_hra_exemption(
            basic_salary_annual=user.monthly_income * 0.5 * 12,
            hra_received_annual=user.monthly_income * 0.4 * 12,
            rent_paid_annual=tool_input.get("rent_paid_annual"),
            is_metro=tool_input.get("is_metro", True)
        )
        return f"HRA exemption: {result}"

    elif tool_name == "calculate_tax_harvesting":
        from calculators.tax_harvesting import calculate_tax_harvesting
        gains = [{"gain": tool_input.get("total_gains"), "holding_months": 13}]
        losses = [{"loss": tool_input.get("total_losses")}]
        result = calculate_tax_harvesting(gains=gains, losses=losses)
        return f"Tax harvesting opportunity: {result}"

    elif tool_name == "calculate_family_tax_arbitrage":
        from calculators.family_tax_arbitrage import calculate_family_tax_arbitrage
        relation = tool_input.get("family_member_relation", "parent")
        family_member = next(
            (m for m in user.family_members if relation.lower() in m.relation.lower()),
            None
        )
        family_bracket = family_member.tax_bracket if family_member else 0
        result = calculate_family_tax_arbitrage(
            investment_amount=tool_input.get("investment_amount"),
            investment_return_percent=tool_input.get("investment_return_percent", 7),
            user_tax_bracket=30,
            family_member_tax_bracket=family_bracket,
            family_member_relation=relation
        )
        return f"Family tax arbitrage: {result}"

    elif tool_name == "calculate_esop_tax":
        from calculators.esop_tax import calculate_esop_tax
        result = calculate_esop_tax(
            vesting_value=tool_input.get("vesting_value"),
            purchase_price=tool_input.get("purchase_price", 0),
            tax_bracket=30
        )
        return f"ESOP tax calculation: {result}"

    return "Tool not found"


def react_tax_agent(state: VaultState) -> VaultState:
    response, core_directive, team_brief = react_engine(
        user=state["user"],
        persona=TAX_PERSONA,
        tools=TAX_TOOLS,
        tool_executor=tax_executor,
        user_query=state.get("user_query", "Analyze my tax situation and tell me how to save maximum tax."),
        state=state
    )
    if response.strip() == "SKIP":
        return {}
    return {
        "agent_memos": {"Tax Optimizer": response},
        "team_awareness": {"Tax Optimizer": team_brief}
    }