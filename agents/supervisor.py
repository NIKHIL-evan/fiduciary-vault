import os
import json
import anthropic
from dotenv import load_dotenv
from schemas.user_profile import SupervisorDecision
from schemas.states import VaultState

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

AGENT_ROSTER = {
    "debt": "Debt Strategist — analyzes debt emergency, balance transfer, prepayment, cheapest capital.",
    "tax": "Tax Optimizer — finds 80C gaps, LTCG/STCG, HRA, family tax arbitrage, ESOP tax.",
    "insurance": "Risk Analyst — identifies insurance gaps, surrender value analysis, premium estimates.",
    "retirement": "Retirement Planner — corpus calculation, EPF projection, education goals, post-retirement income.",
    "investment": "Investment Advisor — SIP allocation, asset allocation, step-up SIP, lumpsum vs STP."
}

def supervisor_node(state: VaultState) -> VaultState:
    user_message = state.get("user_query", "Give me a complete financial analysis.")
    
    # Include financial health context for better routing
    health = state.get("health_score", {})
    financial_health = state.get("financial_health", "UNKNOWN")
    surplus = state.get("investable_surplus", "unknown")

    roster_text = "\n".join(
        f"- {name}: {desc}"
        for name, desc in AGENT_ROSTER.items()
    )

    prompt = f"""You are a routing supervisor for a financial advisory system.

User's financial snapshot:
- Monthly Income: ₹{state['user'].monthly_income}
- Monthly Expense: ₹{state['user'].monthly_expense}
- Existing Debts: {len(state['user'].existing_debts)}
- Tax Regime: {state['user'].tax_regime}
- Financial Health: {financial_health}
- Investable Surplus: ₹{surplus}
- Health Score: {health.get('total_score', 'N/A')}/100

Available specialist agents (Fiduciary already ran and set the anchor):
{roster_text}

User's question: {user_message}

ROUTING RULES:
1. Full analysis or "what should I do" → include all 5 agents
2. Specific question → only relevant agents (max 2-3)
3. Always respect financial health — if EMERGENCY, debt agent is mandatory
4. Agent names must exactly match: debt, tax, insurance, retirement, investment

Respond ONLY in this JSON format, nothing else:
{{
    "agents_to_call": ["agent1", "agent2"],
    "reasoning": "why these agents were selected"
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text
    parsed = json.loads(response_text)
    decision = SupervisorDecision(**parsed)

    return {
        "supervisor_decision": {
            "agents_to_call": decision.agents_to_call,
            "reasoning": decision.reasoning
        },
        "active_agents": decision.agents_to_call
    }