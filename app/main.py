# app/main.py
from fastapi import FastAPI
from app.api.v1 import auth, chat
import logging
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI application starting up.........................")
    yield
    logger.info("FastAPI application shutting down...")

app = FastAPI(title="AI Agent API", lifespan=lifespan)

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(chat.router, prefix="/api/v1/chat")

@app.get("/")
def root():
    logger.info("API is running")
    return {"message": "API is running"}
