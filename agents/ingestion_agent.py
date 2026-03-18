import requests
import os
from schemas.states import VaultState
from schemas.user_profile import InvestmentProfile

CASPARSER_API_KEY = os.environ.get("CASPARSER_API_KEY", "sandbox-with-json-responses")
API_URL = "https://api.casparser.in/v4/smart/parse"

def ingestion_agent(state: VaultState) -> VaultState:
    user = state["user"]
    pdf_path = state.get("cas_pdf_path")

    if not pdf_path:
        return {**state, "ingestion_status": "NO_PDF"}

    with open(pdf_path, "rb") as f:
        response = requests.post(
            API_URL,
            headers={"x-api-key": CASPARSER_API_KEY},
            files={"file": f},
            data={"password": state.get("pdf_password", "")},
            timeout=60
        )

    data = response.json()

    if data.get("status") == "failed":
        return {**state, "ingestion_status": "FAILED"}

    mutual_funds = data.get("mutual_funds", [])
    investments = [
        InvestmentProfile(
            investment_type=fund["scheme_name"],
            annual_amount=float(fund.get("value", 0))
        )
        for fund in mutual_funds
    ]

    user.existing_investments = investments

    return {
        **state,
        "user": user,
        "ingestion_status": "SUCCESS",
        "total_portfolio_value": data["summary"]["total_value"]
    }