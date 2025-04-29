# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, chat, incidents
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

ORIGINS = [
    "http://localhost:5173",
]

# Add CORS middleware with logging
logger.info("Adding CORS middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,  # Allow credentials
    allow_methods=["*"],
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)
logger.info("CORS middleware added successfully")

# Middleware to log incoming requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    # logger.info(f"Request headers: {request.headers}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    # logger.info(f"Response headers: {response.headers}")
    return response

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(chat.router, prefix="/api/v1/chat")
app.include_router(incidents.router, prefix="/api/v1/incidents")

@app.get("/")
def root():
    logger.info("API is running")
    return {"message": "API is running"}
