from typing import TypedDict, Optional, Annotated
import operator
from schemas.user_profile import UserFinancialProfile

class VaultState(TypedDict):
    # Core user data
    user: UserFinancialProfile
    
    # Ingestion
    cas_pdf_path: Optional[str]
    pdf_password: Optional[str]
    ingestion_status: Optional[str]
    total_portfolio_value: Optional[float]
    
    # Supervisor
    supervisor_decision: Optional[dict]
    active_agents: Optional[list]
    
    # Agent memos - each agent writes here
    agent_memos: Annotated[dict, operator.or_]
    
    # Final output
    final_report: Optional[str]

    user_query: Optional[str]