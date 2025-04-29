import logging
import asyncio
from app.services.faiss_connector import search_evidence, search_law
from app.services.bm25_searcher import load_documents_via_session, BM25Retriever
from app.services.hybrid_search_reranker import rerank_with_cross_encoder_async

logger = logging.getLogger(__name__)


async def hybrid_retrieve_and_rerank(query: str, session, top_k_retrieve_each: int = 10, top_k_final: int = 5) -> list:
    """
    Hybrid retrieval (FAISS + BM25) + Cross-Encoder reranking (Session version).

    :param query: User query text
    :param session: SQLAlchemy Session
    :param top_k_retrieve_each: How many documents retrieved per retriever
    :param top_k_final: How many documents to return after reranking
    :return: Top reranked documents
    """

    logger.info(f"Starting hybrid retrieval for query: '{query}'")

    # --- 1. FAISS Retrieval ---
    faiss_evidence_results = search_evidence(session, query, top_k=top_k_retrieve_each)
    faiss_law_results = search_law(session, query, top_k=top_k_retrieve_each)
    faiss_results = faiss_evidence_results + faiss_law_results
    logger.info(f"FAISS retrieval completed: {len(faiss_results)} documents.")

    # --- 2. BM25 Retrieval (Session version) ---
    documents = load_documents_via_session(session)
    bm25_retriever = BM25Retriever(documents)
    bm25_results = bm25_retriever.retrieve(query, top_k=top_k_retrieve_each)
    logger.info(f"BM25 retrieval completed: {len(bm25_results)} documents.")

    # --- 3. Merge & Deduplicate ---
    initial_documents = faiss_results + bm25_results
    unique_docs = {doc['id']: doc for doc in initial_documents}.values()
    logger.info(f"Deduplication completed: {len(unique_docs)} unique documents.")

    # --- 4. Async Reranking ---
    logger.info("Starting Cross-Encoder reranking...")
    reranked_documents = await rerank_with_cross_encoder_async(query, list(unique_docs), top_k=top_k_final)
    logger.info(f"Reranking completed: Top-{top_k_final} documents selected.")

    return reranked_documents

