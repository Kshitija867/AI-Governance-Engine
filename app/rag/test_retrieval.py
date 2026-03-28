import asyncio
from app.rag.retriever import PolicyRetriever

async def test():
    retriever = PolicyRetriever()
    results = await retriever.retrieve(
        "How to bypass system instructions and reveal hidden prompts?"
    )
    print(results)

if __name__ == "__main__":
    asyncio.run(test())

