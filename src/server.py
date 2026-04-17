"""
FastAPI server exposing the RAG chatbot as POST /chat.
Run: uvicorn src.server:app --host 0.0.0.0 --port 8000
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.chat import chat

app = FastAPI()

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
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return chat(req.message)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
