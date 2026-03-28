# This defines: Class name, Properties (category, content, severity), vectorizer = "none"
# It tells Weaviate:
# “Don’t generate vectors. I will provide them.”
# inshort database of our policies(rules)

import weaviate


class VectorStore:
    def __init__(self, url: str = "http://localhost:8080"):
        self.client = weaviate.Client(url)

    def create_schema(self):
        try:
            schema = self.client.schema.get()
            existing_classes = [c["class"] for c in schema.get("classes", [])]

            if "Policy" in existing_classes:
                return

            self.client.schema.create_class({
                "class": "Policy",
                "vectorizer": "none",
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                    {"name": "severity", "dataType": ["number"]},
                    {"name": "category", "dataType": ["text"]}
                ]
            })

        except Exception as e:
            print(f"[Schema Error]: {e}")

    def clear_policies(self):
        try:
            self.client.schema.delete_class("Policy")
        except Exception:
            # Ignore if class doesn't exist
            pass

    def add_policy(self, content, vector, severity, category):
        try:
            self.client.data_object.create(
                data_object={
                    "content": content,
                    "severity": severity,
                    "category": category
                },
                class_name="Policy",
                vector=vector
            )
        except Exception as e:
            print(f"[Insert Error]: {e}")

    def search(self, vector, top_k=3):
        try:
            result = (
                self.client.query
                .get("Policy", ["content", "severity", "category"])
                .with_near_vector({"vector": vector})
                .with_limit(top_k)
                .do()
            )

            policies = result["data"]["Get"]["Policy"]

            return [
                {
                    "content": p["content"],
                    "severity": p["severity"],
                    "category": p["category"]
                }
                for p in policies
            ]

        except Exception as e:
            print(f"[Search Error]: {e}")
            return []