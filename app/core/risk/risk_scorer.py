class RiskScorer:

    def compute_risk(self, injection_score: float, policy_relevance: float) -> float:
        """
        Combine injection risk + policy relevance.
        Higher injection = higher risk.
        Lower policy match = higher risk.
        """

        risk = (0.7 * injection_score) + (0.3 * (1 - policy_relevance))
        return min(risk, 1.0)