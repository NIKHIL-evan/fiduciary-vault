import os
import anthropic
from dotenv import load_dotenv
from schemas.user_profile import UserFinancialProfile

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def extract_briefs(response: str) -> tuple:
    lines = response.split('\n')
    core_directive = ""
    team_brief = ""
    clean_lines = []
    
    for line in lines:
        if line.strip().startswith("CORE_DIRECTIVE:"):
            core_directive = line.replace("CORE_DIRECTIVE:", "").strip()
        elif line.strip().startswith("TEAM_BRIEF:"):
            team_brief = line.replace("TEAM_BRIEF:", "").strip()
        else:
            clean_lines.append(line)
    
    clean_response = "\n".join(clean_lines).strip()
    return clean_response, core_directive, team_brief

def react_engine(
    user: UserFinancialProfile,
    persona: str,
    tools: list,
    tool_executor,
    user_query: str,
    state: dict = {}
) -> tuple:
    
    team_awareness = state.get("team_awareness", {})
    logic_anchor = state.get("logic_anchor", "")
    previous_memos = state.get("agent_memos", {})
    
    team_context = ""
    if logic_anchor:
        team_context += f"\nCORE DIRECTIVE FROM CHIEF FIDUCIARY:\n{logic_anchor}\n"
    
    if team_awareness:
        team_context += "\nTEAM AWARENESS:\n"
        for specialist, brief in team_awareness.items():
            team_context += f"{specialist}: {brief}\n"

    financial_context = ""
    if state.get("investable_surplus") is not None:
        health = state.get("health_score") or {}
        risk = state.get("risk_assessment") or {}
        emergency = state.get("emergency_fund_status") or {}
        nw = state.get("net_worth_data") or {}
        goal = state.get("goal_allocation") or {}

        financial_context = f"""
    VERIFIED FINANCIAL TRUTH (trust these numbers):
    - Monthly Surplus: ₹{state.get('investable_surplus')}
    - Financial Health: {state.get('financial_health')}
    - Health Score: {health.get('total_score', 'N/A')}/100 ({health.get('grade', 'N/A')} - {health.get('status', 'N/A')})
    - Risk Profile: {risk.get('risk_profile', 'N/A')} (Score: {risk.get('risk_score', 'N/A')}/100)
    - Emergency Fund: {emergency.get('months_covered', 'N/A')} months covered ({emergency.get('status', 'N/A')})
    - Net Worth: ₹{nw.get('net_worth', 'N/A')} ({nw.get('net_worth_health', 'N/A')})
    - Goal Allocation: {goal.get('allocations', 'N/A')}
    - Debt Priority: {state.get('debt_priority', 'N/A')}
    """

    messages = [
        {
            "role": "user",
            "content": f"""Client Profile:
                            Name: {user.name}
                            Age: {user.age}
                            Monthly Income: ₹{user.monthly_income}
                            Monthly Expense: ₹{user.monthly_expense}
                            Debts: {[f"{d.debt_type} at {d.interest_rate}%" for d in user.existing_debts]}
                            Family: {[f"{m.relation} age {m.age}, expense ₹{m.monthly_expense}" for m in user.family_members if m.is_dependent]}
                            Investments: {[f"{i.investment_type}: ₹{i.annual_amount}" for i in user.existing_investments]}
                            Tax Regime: {user.tax_regime}
                            {financial_context}
                            {team_context}
                            Query: {user_query}

                            Use your tools first. Then respond."""
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=persona,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            raw_response = response.content[0].text
            clean_response, core_directive, team_brief = extract_briefs(raw_response)
            return clean_response, core_directive, team_brief

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = tool_executor(block.name, block.input, user)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "user", "content": tool_results})