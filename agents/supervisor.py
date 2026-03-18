import os
import json
import anthropic
from dotenv import load_dotenv
from schemas.user_profile import SupervisorDecision
from schemas.states import VaultState

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

AGENT_ROSTER = {
    "fiduciary": "Assesses complete financial situation, blocks harmful decisions, gives overall verdict.",
    "debt": "Analyzes debt emergency, calculates surplus, creates debt repayment plan.",
    "tax": "Finds unused tax saving opportunities, calculates exact rupee savings under 80C.",
    "insurance": "Identifies critical life and health insurance gaps, quantifies family risk.",
    "retirement": "Calculates inflation-adjusted retirement corpus and required monthly SIP.",
    "sip": "Creates investment plan, recommends SIP allocation based on goals and surplus."
}

def supervisor_node(state: VaultState) -> VaultState:
    user_message = state.get("user_query", "Give me a complete financial analysis.")
    
    roster_text = "\n".join(
        f"- {name}: {desc}"
        for name, desc in AGENT_ROSTER.items()
    )

    prompt = f"""You are a financial supervisor managing a team of specialist agents.

User's financial snapshot:
- Monthly Income: ₹{state['user'].monthly_income}
- Monthly Expense: ₹{state['user'].monthly_expense}
- Existing Debts: {len(state['user'].existing_debts)}
- Tax Regime: {state['user'].tax_regime}

Available agents:
{roster_text}

User's question: {user_message}

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
        "supervisor_decision": {"agents_to_call": decision.agents_to_call, "reasoning": decision.reasoning},
        "active_agents": decision.agents_to_call
    }