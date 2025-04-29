import aiohttp
import asyncio
import json
import logging
from app.config.config import OPENAI_API_KEY as EMBEDDING_MODEL_API_KEY

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Async Cross-Encoder Reranking ---
async def fetch_score(session: aiohttp.ClientSession, api_key: str, model: str, query: str, description: str) -> float:
    """Send a single scoring request asynchronously."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": f"根据以下query评估文本相关性，给出0到1之间的相关性分数。\n\nQuery: {query}\nText: {description}"}
        ],
        "temperature": 0,
        "max_tokens": 10
    }

    try:
        async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=20)) as response:
            if response.status != 200:
                logger.warning(f"Scoring request failed with status {response.status}")
                return 0.0
            data = await response.json()
            try:
                score_text = data['choices'][0]['message']['content'].strip()
                score = float(score_text)
                return min(max(score, 0.0), 1.0)  # 保证分数在0-1之间
            except (KeyError, ValueError) as e:
                logger.warning(f"Failed to parse score from response: {e}")
                return 0.0
    except Exception as e:
        logger.error(f"Request exception: {e}")
        return 0.0

async def rerank_with_cross_encoder_async(query: str, documents: list, top_k: int = 5, api_key: str = EMBEDDING_MODEL_API_KEY, model: str = "gpt-3.5-turbo") -> list:
    """
    Concurrently rerank documents using Cross-Encoder (via OpenAI API), return top-k documents with scores.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for doc in documents:
            tasks.append(fetch_score(session, api_key, model, query, doc['description']))

        scores = await asyncio.gather(*tasks)

    # Attach scores to documents
    scored_documents = []
    for doc, score in zip(documents, scores):
        scored_documents.append({
            **doc,
            "rerank_score": score
        })

    # Sort by rerank_score descending
    scored_documents = sorted(scored_documents, key=lambda x: x['rerank_score'], reverse=True)[:top_k]
    return scored_documents

