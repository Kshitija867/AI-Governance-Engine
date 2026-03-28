# Retrieval is the process of finding semantically similar stored vectors based on a query vector
# This is the runtime search phase.
# This runs every time a user asks something.
# converts user query to vector
# search weaviate


from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


class PolicyRetriever:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.store = VectorStore()

    async def retrieve(self, query: str, top_k: int = 3):
        if not query:
            return []

        try:
            vector = await self.embedder.embed(query)
            results = self.store.search(vector, top_k)

            print("Retrieved Policies:", results)  # DEBUG LINE

            return results

        except Exception as e:
            print(f"[Retriever Error]: {e}")
            return []
