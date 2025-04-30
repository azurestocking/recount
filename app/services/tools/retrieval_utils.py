from app.services.hybrid_search import hybrid_retrieve_and_rerank
from app.services.graph_expansion_searcher import expand_neighbors
from app.services.graph_rag_generator import select_best_chain, build_prompt_from_chain

# Perform FAISS + BM25 retrieval and reranking
async def perform_hybrid_search(query: str, session, top_k_retrieve_each: int = 10, top_k_final: int = 5):
    documents = await hybrid_retrieve_and_rerank(query, session, top_k_retrieve_each, top_k_final)
    return documents

# Expand graph neighbors, select best reasoning chain, and build reasoning prompt.
async def perform_graph_reasoning(retrieved_docs: list, session, user_query: str):
    graph = expand_neighbors(session, retrieved_docs)
    if not graph["nodes"]:
        return (
            "Sorry, based on current evidence and laws, we could not find sufficient information to reason about your query."
        )
    best_chain = select_best_chain(graph, top_k_start_nodes=5)
    prompt = build_prompt_from_chain(best_chain, graph, user_query)
    return prompt
