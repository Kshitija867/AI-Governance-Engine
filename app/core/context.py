from typing import List, Optional

class GovernanceContext:
    def __init__(self, user_id: str, role: str, query: str):
        self.user_id = user_id
        self.role = role.lower()
        self.query = query

        self.risk_score: Optional[float] = None
        self.policy_flags: List[str] = []



