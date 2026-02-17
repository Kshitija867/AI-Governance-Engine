from app.models.enums import DecisionType
from app.core.context import GovernanceContext

class DecisionEngine:

    def decide(self, context: GovernanceContext) -> DecisionType:

        if context.risk_score is None:
            raise ValueError("Risk score must be calculated before decision.")

        if context.risk_score >= 0.8:
            return DecisionType.ESCALATE
        elif context.risk_score >= 0.5:
            return DecisionType.REFUSE
        elif context.risk_score >= 0.3:
            return DecisionType.REWRITE
        else:
            return DecisionType.ALLOW
