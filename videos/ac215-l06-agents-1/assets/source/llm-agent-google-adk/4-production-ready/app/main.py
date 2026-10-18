"""
Simple FastAPI Application for ADK Agent
"""

import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.agent import agent
from app.runner import runner

app = FastAPI()


class ChatRequest(BaseModel):
    user_message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Non-streaming endpoint - returns complete response"""
    response_text = await runner.run(request.user_message)
    return ChatResponse(response=response_text)


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming endpoint - streams response as it's generated"""

    async def event_generator():
        async for chunk in runner.run_stream(request.user_message):
            yield json.dumps({"chunk": chunk}) + "\n"

     # can be media_type="text/event-stream" or "text/plain". Change depending on your front-end
    return StreamingResponse(event_generator(), media_type="application/x-ndjson")
