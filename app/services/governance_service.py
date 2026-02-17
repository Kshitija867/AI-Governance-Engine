from app.core.context import GovernanceContext
from app.core.result import GovernanceResult
from app.core.risk.base import RiskScorer
from app.core.decision_engine import DecisionEngine
from app.models.enums import DecisionType
from app.services.llm_service import LLMService

class GovernanceService:

    def __init__(
        self,
        risk_scorer: RiskScorer,
        decision_engine: DecisionEngine,
        llm_service: LLMService
    ):
        self.risk_scorer = risk_scorer
        self.decision_engine = decision_engine
        self.llm_service = llm_service

    async def evaluate(self, user_id: str, role: str, query: str) -> GovernanceResult:

        context = GovernanceContext(user_id, role, query)

        # 1. Risk
        self.risk_scorer.calculate(context)

        # 2. Decision
        decision = self.decision_engine.decide(context)

        # 3. Action
        if decision == DecisionType.ALLOW:
            response = await self.llm_service.generate(query)
        elif decision == DecisionType.REWRITE:
            response = "Response rewritten due to moderate risk."
        elif decision == DecisionType.REFUSE:
            response = "Request refused due to policy violation."
        else:
            response = "Escalated to human review."

        return GovernanceResult(context, decision, response)
