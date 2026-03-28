
class InjectionRiskScorer:

    SUSPICIOUS_PATTERNS = [
        "ignore previous instructions",
        "reveal system prompt",
        "disregard policies",
        "bypass safety",
        "act as root"
    ]

    MALICIOUS_PATTERNS = [
        "hack",
        "password",
        "break into",
        "exploit",
        "steal data",
        "unauthorized access",
        "bypass authentication",
        "disable security",
        "disable audit",
        "firewall",
        "admin account",
        "bypass",
        "delete logs",
        "exploit admin",
        "bypass firewall"
    ]

    def calculate(self, context):

        query_lower = context.query.lower()

        injection_score = 0.0
        malicious_score = 0.0


        # Detect injection patterns
        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern in query_lower:
                injection_score += 0.8

        injection_score = min(injection_score, 1.0)

        # Detect malicious intent patterns
        for pattern in self.MALICIOUS_PATTERNS:
            if pattern in query_lower:
                malicious_score += 0.7



        malicious_score = min(malicious_score, 1.0)

        # Policy relevance
        policy_score = 1.0 if context.policies else 0.3
        role_penalty = 0.5 if getattr(context, "role_violation", False) else 0.0

        # Updated risk formula (slightly adjusted weights)
        risk = (
            0.4 * injection_score +
            0.6 * malicious_score +
            0.1 * (1 - policy_score) +
            role_penalty
        )

        # Update context
        context.injection_score = injection_score
        context.malicious_score = malicious_score
        context.policy_score = policy_score
        context.risk_score = min(risk, 1.0)
        


        