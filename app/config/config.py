# core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DATABASE_URL: str = "mysql://root:zhongkao0617@localhost:3306/lawagentdb"
    DATABASE_URL: str = "mysql+pymysql://root:20020329@127.0.0.1:3306/victim_ai_db"
    # "mysql://{user}:{password}@localhost:3306/{database_name}"
    # "mysql+pymysql://root:password123@localhost:3306/victim_ai_db"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Agent"
    MODEL_ACCESS_KEY: str = "sk-proj-1234567890"

    class Config:
        env_file = ".env"

# 添加所有API密钥和配置
OPENAI_API_KEY = "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"

settings = Settings()
