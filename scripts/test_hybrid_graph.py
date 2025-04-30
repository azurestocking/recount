import asyncio
from app.services.tools.retrieval_utils import perform_hybrid_search, perform_graph_reasoning
from app.models.database import SessionLocal
import nltk

nltk.download('punkt', quiet=True)

async def test_hybrid_and_graph():
    session = SessionLocal()
    user_query = "A dispute regarding property ownership evidence"

    print("🔍 Running Hybrid Search...")

    retrieved_docs = await perform_hybrid_search(user_query, session, top_k_retrieve_each=10, top_k_final=5)

    print(f"✅ Retrieved {len(retrieved_docs)} documents.")
    for i, doc in enumerate(retrieved_docs):
        print(f"{i+1}. ({doc['type']}) {doc['description']} (Score: {doc.get('rerank_score', 0):.4f})")

    print("\n🧠 Running Graph Reasoning...")

    reasoning_prompt = await perform_graph_reasoning(retrieved_docs, session, user_query)

    print("\n=== Reasoning Prompt ===")
    print(reasoning_prompt)

    session.close()

if __name__ == "__main__":
    asyncio.run(test_hybrid_and_graph())

