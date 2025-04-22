from functools import lru_cache
from app.services.aiAgent import AIAgent
from app.config.config import settings

@lru_cache()
def get_ai_agent():
    return AIAgent(settings.DATABASE_URL)
