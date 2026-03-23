from pydantic import BaseModel, Field
from typing import List, Optional

class DebtProfile(BaseModel):
    debt_type: str
    amount: float = Field(..., gt=0)
    interest_rate: float = Field(..., ge=0)
    min_payment: float = Field(..., gt=0)

class InvestmentProfile(BaseModel):
    investment_type: str
    annual_amount: float

class SupervisorDecision(BaseModel):
    agents_to_call: List[str]
    reasoning: str

class LiquidityEvent(BaseModel):
    purpose: str
    amount_needed: float
    target_year: int

class ExistingPolicy(BaseModel):
    policy_type: str        # "ULIP", "endowment", "term", "health"
    annual_premium: float
    surrender_value: float
    maturity_year: int
    coverage_amount: float

LIQUIDITY_SCORES = {
    "savings_account": 10,
    "liquid_fund": 9,
    "fd": 8,
    "recurring_deposit": 8,
    "gold": 7,
    "sovereign_gold_bond": 7,
    "debt_fund": 7,
    "equity_fund": 6,
    "elss": 5,
    "ppf": 3,
    "epf": 2,
    "nps": 2,
    "property": 1,
    "vehicle": 2,
    "land": 1
}
class IlliquidAsset(BaseModel):
    asset_type: str
    estimated_value: float
    liquidity_score: Optional[int] = None

    def get_liquidity_score(self) -> int:
        if self.liquidity_score is not None:
            return self.liquidity_score
        return LIQUIDITY_SCORES.get(self.asset_type.lower(), 5)

class FamilyMember(BaseModel):
    relation: str
    age: int
    monthly_expense: float = 0      # from DependentProfile
    is_dependent: bool = False       # do you support them financially?
    monthly_income: float = 0        # their own income
    tax_bracket: float = 0 

class UserFinancialProfile(BaseModel):
    name: str
    age: int
    monthly_income: float
    monthly_expense: float
    family_members: List[FamilyMember] = []
    existing_debts: List[DebtProfile] = []
    assets_owned: List[str] = []
    retirement_age: int = 60
    tax_regime: str = "new"
    term_insurance_cover: float = 0
    health_insurance_cover: float = 0
    existing_investments: List[InvestmentProfile] = []
    epf_balance: float = 0
    credit_score: Optional[int] = None
    risk_profile: Optional[str] = None  # "CONSERVATIVE", "MODERATE", "AGGRESSIVE"
    esop_rsu_value: float = 0
    liquidity_events: List[LiquidityEvent] = []
    existing_policies: List[ExistingPolicy] = []
    illiquid_assets: List[IlliquidAsset] = []
