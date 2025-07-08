from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import auth
from databases.db import engine
from models import user as user_model
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    user_model.Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title="RAG Chatbot",
    description="Self hosted RAF Chatbot using local LLMs",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["users"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
