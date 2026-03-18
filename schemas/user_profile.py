from pydantic import BaseModel, Field
from typing import List, Any 

class DebtProfile(BaseModel):
    debt_type: str
    amount: float = Field(..., gt=0)
    interest_rate: float = Field(..., ge=0)
    min_payment: float = Field(..., gt=0)

class DependentProfile(BaseModel):
    relation: str
    age: int
    monthly_expense: float

class InvestmentProfile(BaseModel):
    investment_type: str
    annual_amount: float

class SupervisorDecision(BaseModel):
    agents_to_call: List[str]
    reasoning: str

class UserFinancialProfile(BaseModel):
    name: str
    age: int
    monthly_income: float
    monthly_expense: float
    dependents: List[DependentProfile] = []
    existing_debts: List[DebtProfile] = []
    assets_owned: List[str] = []
    retirement_age: int = 60
    tax_regime: str = "new"
    term_insurance_cover: float = 0
    health_insurance_cover: float = 0
    existing_investments: List[InvestmentProfile] = []

