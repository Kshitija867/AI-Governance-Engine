class MetricsCollector:

    def __init__(self):
        self.total_requests = 0
        self.allow = 0
        self.rewrite = 0
        self.refuse = 0
        self.high_risk = 0
        self.medium_risk = 0
        self.low_risk = 0
        self.total_risk = 0.0

    def update(self, result):

        self.total_requests += 1
        risk = result.context.risk_score
        self.total_risk += risk

        if result.decision.name == "ALLOW":
            self.allow += 1
        elif result.decision.name == "REWRITE":
            self.rewrite += 1
        elif result.decision.name == "REFUSE":
            self.refuse += 1

        # Risk bucket tracking
        if risk >= 0.75:
            self.high_risk += 1
        elif risk >= 0.4:
            self.medium_risk += 1
        else:
            self.low_risk += 1

    def summary(self):

        avg_risk = (
            self.total_risk / self.total_requests
            if self.total_requests else 0
        )

        return {
            "total_requests": self.total_requests,
            "allow": self.allow,
            "rewrite": self.rewrite,
            "refuse": self.refuse,
            "average_risk": round(avg_risk, 3),
            "risk_distribution": {
                "high": self.high_risk,
                "medium": self.medium_risk,
                "low": self.low_risk
            }
        }