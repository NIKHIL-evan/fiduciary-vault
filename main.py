from langgraph.graph import StateGraph
from schemas.states import VaultState
from agents.ingestion_agent import ingestion_agent
from agents.react_fiduciary_agent import react_fiduciary_agent
from agents.react_debt_agent import react_debt_agent
from agents.react_tax_agent import react_tax_agent
from agents.react_insurance_agent import react_insurance_agent
from agents.react_retirement_agent import react_retirement_agent
from agents.react_investment_agent import react_investment_agent
from agents.supervisor import supervisor_node
from schemas.user_profile import UserFinancialProfile, DebtProfile, InvestmentProfile, FamilyMember
from langgraph.checkpoint.memory import MemorySaver

def make_node(agent_fn, agent_name: str):
    def node(state: VaultState) -> VaultState:
        active_agents = state.get("active_agents")
        if active_agents and agent_name not in active_agents:
            return {}
        return agent_fn(state)
    return node

# Build graph
graph = StateGraph(VaultState)
graph.add_node("ingestion", ingestion_agent)
graph.add_node("fiduciary", react_fiduciary_agent)
graph.add_node("supervisor", supervisor_node)
graph.add_node("debt", make_node(react_debt_agent, "debt"))
graph.add_node("tax", make_node(react_tax_agent, "tax"))
graph.add_node("insurance", make_node(react_insurance_agent, "insurance"))
graph.add_node("retirement", make_node(react_retirement_agent, "retirement"))
graph.add_node("investment", make_node(react_investment_agent, "investment"))

graph.set_entry_point("ingestion")
graph.add_edge("ingestion", "fiduciary")
graph.add_edge("fiduciary", "supervisor")
graph.add_edge("supervisor", "debt")
graph.add_edge("debt", "tax")
graph.add_edge("tax", "insurance")
graph.add_edge("insurance", "retirement")
graph.add_edge("retirement", "investment")
graph.set_finish_point("investment")

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

rajesh = UserFinancialProfile(
    name="Rajesh Kumar",
    age=38,
    monthly_income=150000,
    monthly_expense=65000,
    term_insurance_cover=5000000,
    health_insurance_cover=300000,
    family_members=[
        FamilyMember(relation="spouse", age=32, monthly_expense=15000, is_dependent=True, tax_bracket=0),
        FamilyMember(relation="child", age=8, monthly_expense=10000, is_dependent=True, tax_bracket=0),
    ],
    existing_debts=[
        DebtProfile(debt_type="credit_card", amount=180000, interest_rate=42, min_payment=5400),
        DebtProfile(debt_type="personal_loan", amount=500000, interest_rate=16, min_payment=12000),
        DebtProfile(debt_type="home_loan", amount=4500000, interest_rate=9.2, min_payment=42000),
        DebtProfile(debt_type="car_loan", amount=800000, interest_rate=11, min_payment=18000)
    ],
    assets_owned=["house", "car", "gold"],
    existing_investments=[
        InvestmentProfile(investment_type="PPF", annual_amount=30000),
        InvestmentProfile(investment_type="ELSS", annual_amount=25000),
        InvestmentProfile(investment_type="NPS", annual_amount=20000),
    ],
    retirement_age=58,
    tax_regime="old"
)

result = app.invoke(
    {
        "user": rajesh,
        "cas_pdf_path": None,
        "pdf_password": "",
        "agent_memos": {},
        "team_awareness": {},
        "user_query": "Give me a complete financial analysis"
    },
    config={"configurable": {"thread_id": "rajesh_123"}}
)

print("\nAgents that ran:")
for agent in result["agent_memos"].keys():
    print(f"  - {agent}")

print("\n" + "="*60)
for agent, response in result["agent_memos"].items():
    print(f"\n[{agent.upper()}]")
    print("="*60)
    print(response)
    print()