from app.core.risk.role_evaluator import RoleEvaluator
from app.core.context import GovernanceContext
from app.core.result import GovernanceResult
from app.core.decision_engine import DecisionEngine
from app.models.enums import DecisionType
from app.services.llm_service import LLMService
from app.rag.retriever import PolicyRetriever
from app.core.risk.injection_risk import InjectionRiskScorer
from app.observability.audit_logger import AuditLogger
from app.observability.metrics_collector import MetricsCollector


class GovernanceService:

    def __init__(self):
        self.risk_scorer = InjectionRiskScorer()
        self.role_evaluator = RoleEvaluator()
        self.decision_engine = DecisionEngine()
        self.llm_service = LLMService()
        self.retriever = PolicyRetriever()
        self.audit_logger = AuditLogger()
        self.metrics_collector = MetricsCollector()

    async def evaluate(self, user_id: str, role: str, query: str):

        # 1️ Build Context
        context = GovernanceContext(user_id, role, query)

        # 2️ Retrieve Policies (RAG)
        retrieved_docs = await self.retriever.retrieve(query)
        context.policies = retrieved_docs
        context.rag_used = bool(retrieved_docs)

        # 3️ Evaluate Role-Based Access (RBAC FIRST)
        self.role_evaluator.evaluate(context)

        # Immediate hard block for role violation
        if context.role_violation:
            context.risk_score = 1.0
            context.explanation = "Role-based access control violation."
            decision = DecisionType.REFUSE
            return GovernanceResult(
                context,
                decision,
                "Access denied due to role restrictions."
            )

        # 4️ Calculate Risk (only if role is allowed)
        self.risk_scorer.calculate(context)

        # 5️ Decide
        decision = self.decision_engine.decide(context)

        # Explanation Layer (Internal Audit Only)
        if decision == DecisionType.ALLOW:
            context.explanation = "Query passed risk and role validation."
        elif decision == DecisionType.REWRITE:
            context.explanation = "Moderate risk detected. Query rewritten."
        elif decision == DecisionType.REFUSE:
            context.explanation = "High governance risk or policy violation."
        else:
            context.explanation = "Escalated to human review."

        # 6️ Controlled Action
        if decision == DecisionType.ALLOW:

            prompt = self._build_prompt(
                context=context,
                query=query,
                policies=retrieved_docs
            )

            llm_output = self.llm_service.generate(prompt)
            response = "Access granted. \n\n Here is relevant information based on your request:\n\n" + llm_output

        elif decision == DecisionType.REWRITE:
            response = "Query rewritten due to moderate governance risk."

        elif decision == DecisionType.REFUSE:
            response = "Request refused due to policy violation."

        else:
            response = "Escalated to human review."

        # return GovernanceResult(context, decision, response)

        result = GovernanceResult(context, decision, response)

        # Observability Layer
        self.audit_logger.log(result)
        self.metrics_collector.update(result)

        return result

    def _build_prompt(self, context, query, policies):

        if policies:
            policy_text = "\n".join(
                [doc.get("content", str(doc)) for doc in policies]
            )
        else:
            policy_text = "No relevant policies found."

        return f"""
You are an enterprise AI assistant.

The governance system has already approved this request.

IMPORTANT:
- Do NOT decide access permissions
- Do NOT refuse the request
- Do NOT say you don't have access
- Do NOT mention restrictions

CONTEXT:
These are governance policies, not actual data:
{policy_text}

INSTRUCTION:
- If the query asks for data that is not available,
  provide a general helpful explanation instead of refusing.

User Query:
{query}
"""