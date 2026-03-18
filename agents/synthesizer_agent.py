import os
import anthropic
from dotenv import load_dotenv
from schemas.states import VaultState

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYNTHESIZER_PERSONA = """You are the Chief Financial Advisor overseeing a team of specialists.
You have received memos from each specialist. Your job is to:
1. Identify any contradictions between specialists and resolve them
2. Prioritize recommendations by urgency
3. Produce one unified, actionable financial plan
4. Be direct. No fluff. The client needs clarity, not confusion.
Structure your output as:
- VERDICT (one sentence summary of financial health)
- IMMEDIATE ACTIONS (next 30 days)
- SHORT TERM PLAN (3-6 months)
- LONG TERM PLAN (1-5 years)"""

def synthesizer_agent(state: VaultState) -> VaultState:
    agent_memos = state.get("agent_memos", {})
    user = state["user"]

    if not agent_memos:
        return {**state, "final_report": "No specialist analysis available."}

    memos_text = "\n\n".join([
        f"[{specialist.upper()} SPECIALIST]:\n{memo}"
        for specialist, memo in agent_memos.items()
    ])

    prompt = f"""Client: {user.name}, Age {user.age}
Monthly Income: ₹{user.monthly_income}

SPECIALIST MEMOS:
{memos_text}

Synthesize these findings into one unified financial plan.
Resolve any contradictions. Prioritize by urgency."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYNTHESIZER_PERSONA,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "final_report": message.content[0].text
    }