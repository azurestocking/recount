# core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql://root:zhongkao0617@localhost:3306/lawagentdb"
    # "mysql://{user}:{password}@localhost:3306/{database_name}"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Agent"
    MODEL_ACCESS_KEY: str = "sk-proj-1234567890"

    class Config:
        env_file = ".env"

settings = Settings()
