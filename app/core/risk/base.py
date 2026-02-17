from abc import ABC, abstractmethod
from app.core.context import GovernanceContext

class RiskScorer(ABC):
    @abstractmethod
    def calculate(self, context: GovernanceContext) -> None:
        pass
