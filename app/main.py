# the traffic controller (API Layer)
# from app.core.risk.keyword_risk import KeywordRiskScorer
from app.core.decision_engine import DecisionEngine
from fastapi import FastAPI
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse
from app.services.governance_service import GovernanceService
from app.services.llm_service import LLMService

app = FastAPI(title="AI Governance Engine")
governance_service = GovernanceService(
    # risk_scorer=KeywordRiskScorer(),
    decision_engine=DecisionEngine(),
    llm_service=LLMService()
)

@app.post("/chat")
async def chat_endpoint(request: dict):
    result = await governance_service.evaluate(
        user_id=request["user_id"],
        role=request["role"],
        query=request["query"]
    )
    return result.to_dict()

@app.get("/")
def home():
    return {"status": "Server Working"}


# python -m app.rag.ingestion_pipeline
# python -m app.test_day4