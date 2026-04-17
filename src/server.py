"""
FastAPI server exposing the RAG chatbot as POST /chat.
Run: uvicorn src.server:app --host 0.0.0.0 --port 8000
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.chat import chat

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("server starting up")
    yield
    logger.info("server shutting down")


app = FastAPI(lifespan=lifespan)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://oskariozan.com",
        "https://www.oskariozan.com",
        "https://instrumental-resolution-recognize-binary.trycloudflare.com",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ],
    allow_methods=["POST", "OPTIONS", "GET"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


@app.post("/chat")
@limiter.limit("10/minute")
def chat_endpoint(request: Request, req: ChatRequest):
    try:
        return chat(req.message)
    except Exception:
        logger.exception("chat failed for message prefix: %r", req.message[:80])
        raise HTTPException(
            status_code=503,
            detail="Chat service is temporarily unavailable. Please try again in a moment.",
        )


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
