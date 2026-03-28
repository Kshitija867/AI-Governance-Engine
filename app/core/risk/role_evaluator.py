class RoleEvaluator:

    ROLE_PERMISSIONS = {
        "admin": ["financial_records", "internal_records"],
        "employee": ["internal_records"],
        "user": []
    }

    def evaluate(self, context):
        query_lower = context.query.lower()

        requested_resource = None

        if "financial" in query_lower:
            requested_resource = "financial_records"
        elif "internal" in query_lower:
            requested_resource = "internal_records"

        if requested_resource:
            allowed = requested_resource in self.ROLE_PERMISSIONS.get(context.role, [])
            context.role_violation = not allowed
        else:
            context.role_violation = False