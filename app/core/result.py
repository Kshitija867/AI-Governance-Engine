from app.models.enums import DecisionType
from app.core.context import GovernanceContext

class GovernanceResult:
    def __init__(
        self,
        context: GovernanceContext,
        decision: DecisionType,
        response: str
    ):
        self.user_id = context.user_id
        self.role = context.role
        self.query = context.query
        self.risk_score = context.risk_score
        self.decision = decision
        self.response = response

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "role": self.role,
            "query": self.query,
            "risk_score": self.risk_score,
            "decision": self.decision.value,
            "response": self.response
        }


