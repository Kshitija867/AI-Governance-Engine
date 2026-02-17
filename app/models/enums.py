from enum import Enum


class DecisionType(str, Enum):
    ALLOW = "ALLOW"
    REWRITE = "REWRITE"
    REFUSE = "REFUSE"
    ESCALATE = "ESCALATE"