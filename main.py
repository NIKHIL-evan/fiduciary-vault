from langgraph.graph import StateGraph
from schemas.states import VaultState
from agents.ingestion_agent import ingestion_agent
from agents.react_fiduciary_agent import react_fiduciary_agent
from agents.react_debt_agent import react_debt_agent
from agents.react_tax_agent import react_tax_agent
from agents.react_insurance_agent import react_insurance_agent
from agents.react_retirement_agent import react_retirement_agent
from agents.react_sip_agent import react_sip_agent
from agents.synthesizer_agent import synthesizer_agent
from schemas.user_profile import UserFinancialProfile, DebtProfile, InvestmentProfile, DependentProfile

# Build graph
graph = StateGraph(VaultState)
graph.add_node("ingestion", ingestion_agent)
graph.add_node("fiduciary", react_fiduciary_agent)
graph.add_node("debt", react_debt_agent)
graph.add_node("tax", react_tax_agent)
graph.add_node("insurance",react_insurance_agent )
graph.add_node("retirement", react_retirement_agent)
graph.add_node("sip", react_sip_agent)
graph.add_node("synthesized_report", synthesizer_agent)

graph.set_entry_point("ingestion")
graph.add_edge("ingestion", "fiduciary")
graph.add_edge("fiduciary", "debt")
graph.add_edge("debt", "tax")
graph.add_edge("tax", "insurance")
graph.add_edge("insurance", "retirement")
graph.add_edge("retirement", "sip")
graph.add_edge("sip", "synthesized_report")
graph.set_finish_point("synthesized_report")

app = graph.compile()

# Test user
rajesh = UserFinancialProfile(
    name="Rajesh Kumar",
    age=35,
    monthly_income=85000,
    monthly_expense=45000,
    term_insurance_cover=2500000,
    health_insurance_cover=500000,
    dependents=[
        DependentProfile(relation="spouse", age=32, monthly_expense=15000),
        DependentProfile(relation="child", age=8, monthly_expense=10000)
    ],
    existing_debts=[
        DebtProfile(debt_type="credit_card", amount=50000, interest_rate=36, min_payment=2500),
        DebtProfile(debt_type="personal_loan", amount=200000, interest_rate=14, min_payment=5000),
        DebtProfile(debt_type="home_loan", amount=2000000, interest_rate=8.5, min_payment=18000)
    ],
    assets_owned=["house"],
    existing_investments=[
        InvestmentProfile(investment_type="PPF", annual_amount=50000)
    ],
    retirement_age=60,
    tax_regime="old"
)

result = app.invoke({
        "user": rajesh,
        "cas_pdf_path": None,
        "pdf_password": "",
        "agent_memos": {}
    })

print("\nAgents that ran:")
for agent in result["agent_memos"].keys():
    print(f"  - {agent}")

print(result["final_report"])