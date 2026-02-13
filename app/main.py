# the traffic controller (API Layer)
from fastapi import FastAPI
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse

app = FastAPI(title="AI Governance Engine")

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    return ChatResponse(
        user_id=request.user_id,
        role=request.role,
        query=request.query,
        decision="ALLOW",
        message="Dummy response - governance not applied yet"
    )
