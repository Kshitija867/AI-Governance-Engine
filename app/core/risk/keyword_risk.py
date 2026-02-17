from app.core.risk.base import RiskScorer
from app.core.context import GovernanceContext

SENSITIVE_KEYWORDS = {"salary", "confidential", "password", "ssn", "bomb", "explosive", "kill", "hate", "attack"}

class KeywordRiskScorer(RiskScorer):
    def calculate(self, context: GovernanceContext) -> None:
        query_lower = context.query.lower()
        risk = 0.0

        for word in SENSITIVE_KEYWORDS:
            if word in query_lower:
                risk += 0.4

        if context.role == "external":
            risk += 0.2

        context.risk_score = min(risk, 1.0)

