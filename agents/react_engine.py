import os
import anthropic
from dotenv import load_dotenv
from schemas.user_profile import UserFinancialProfile

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def react_engine(
    user: UserFinancialProfile,
    persona: str,
    tools: list,
    tool_executor,
    user_query: str,
    state: dict 
) -> str:
    previous_memos = state.get("agent_memos", {})
    
    memo_context = ""
    if previous_memos:
        memo_context = "\n\nPrevious specialist findings:\n"
        for specialist, memo in previous_memos.items():
            memo_context += f"\n[{specialist.upper()}]:\n{memo}\n"

    messages = [
        {
            "role": "user",
            "content": f"""Client Profile:
Name: {user.name}
Age: {user.age}
Monthly Income: ₹{user.monthly_income}
Monthly Expense: ₹{user.monthly_expense}
Debts: {[f"{d.debt_type} at {d.interest_rate}%" for d in user.existing_debts]}
Dependents: {[f"{d.relation} age {d.age}, expense ₹{d.monthly_expense}" for d in user.dependents]}
Investments: {[f"{i.investment_type}: ₹{i.annual_amount}" for i in user.existing_investments]}
Tax Regime: {user.tax_regime}
{memo_context}
Query: {user_query}

Use your tools first. Then give your specialist advice."""
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
            return response.content[0].text

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