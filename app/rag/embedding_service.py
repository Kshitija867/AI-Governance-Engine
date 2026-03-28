# imported "all-MiniLM-L6-v2" - it is an embedding model which converts text into vectors.
#  Through this file we can change the model however we want!

from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        # 384-dimensional embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    async def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()


