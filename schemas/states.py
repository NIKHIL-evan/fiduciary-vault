from typing import TypedDict, Optional, Annotated
import operator
from langgraph.graph.message import add_messages
from schemas.user_profile import UserFinancialProfile

class VaultState(TypedDict):
    # Core user data
    user: UserFinancialProfile

    # Ingestion
    cas_pdf_path: Optional[str]
    pdf_password: Optional[str]
    ingestion_status: Optional[str]
    total_portfolio_value: Optional[float]

    # Financial truth (set by Fiduciary)
    investable_surplus: Optional[float]
    debt_priority: Optional[dict]
    financial_health: Optional[str]
    risk_assessment: Optional[dict]
    goal_allocation: Optional[dict]
    emergency_fund_status: Optional[dict]
    net_worth_data: Optional[dict]
    health_score: Optional[dict]

    # Supervisor
    supervisor_decision: Optional[dict]
    active_agents: Optional[list]
    user_query: Optional[str]
    logic_anchor: Optional[str]

    # Agent communication
    agent_memos: Annotated[dict, operator.or_]
    team_awareness: Annotated[dict, operator.or_]

    # Memory
    messages: Annotated[list, add_messages]
    running_summary: Optional[str]

    # Final output
    final_report: Optional[str]