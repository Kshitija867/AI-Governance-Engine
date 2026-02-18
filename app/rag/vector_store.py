# This defines: Class name, Properties (category, content, severity), vectorizer = "none"
# It tells Weaviate:
# “Don’t generate vectors. I will provide them.”
# inshort database of our policies(rules)

import weaviate

class VectorStore:
    def __init__(self):
        self.client = weaviate.Client("http://localhost:8080")

    def create_schema(self):
        if self.client.schema.exists("Policy"):
            return

        schema = {
            "class": "Policy",
            "vectorizer": "none",  # we supply vectors manually
            "properties": [
                {"name": "content", "dataType": ["text"]},
                {"name": "severity", "dataType": ["number"]},
                {"name": "category", "dataType": ["text"]}
            ]
        }

        self.client.schema.create_class(schema)

    def add_policy(self, content, vector, severity, category):
        self.client.data_object.create(
            data_object={
                "content": content,
                "severity": severity,
                "category": category
            },
            class_name="Policy",
            vector=vector
        )

    def search(self, vector, top_k=3):
        result = (
            self.client.query
            .get("Policy", ["content", "severity", "category"])
            .with_near_vector({"vector": vector})
            .with_limit(top_k)
            .do()
        )

        return result["data"]["Get"]["Policy"]
