import json
import os
from datetime import datetime, UTC

class AuditLogger:

    def __init__(self, file_path=None):
                if file_path is None:
                    base_dir = os.getcwd()
                    file_path = os.path.join(base_dir, "governance_audit.log")

                self.file_path = file_path

    def log(self, result):
        context = result.context

        print("Audit logger called") 
        print("Logging to:", self.file_path)

        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),

            # Identity
            "user_id": context.user_id,
            "role": context.role,
            # Query
            "query": context.query,

            # Scores
            "injection_score": context.injection_score,
            "malicious_score": getattr(context, "malicious_score", 0.0),
            "risk_score": context.risk_score,

            # Governance
            "decision": result.decision.name,
            "role_violation": getattr(context, "role_violation", False),
            "policy_count": len(context.policies or []),

            # Explanation layer (internal only)
            "decision_explanation": getattr(context, "explanation", None),

            # RAG Trace
            "rag_enabled": getattr(context, "rag_used", False)
        }

        with open(self.file_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")