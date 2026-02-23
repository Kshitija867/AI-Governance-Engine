class InjectionRiskScorer:

    SUSPICIOUS_PATTERNS = [
        "ignore previous instructions",
        "reveal system prompt",
        "disregard policies",
        "bypass safety",
        "act as root"
    ]

    def calculate(self, context):

        query_lower = context.query.lower()

        injection_score = 0.0
        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern in query_lower:
                injection_score += 0.3

        injection_score = min(injection_score, 1.0)

        # Policy relevance
        policy_score = 1.0 if context.policies else 0.3

        # Final risk formula
        risk = (0.7 * injection_score) + (0.3 * (1 - policy_score))

        # Update context
        context.injection_score = injection_score
        context.policy_score = policy_score
        context.risk_score = min(risk, 1.0)




        