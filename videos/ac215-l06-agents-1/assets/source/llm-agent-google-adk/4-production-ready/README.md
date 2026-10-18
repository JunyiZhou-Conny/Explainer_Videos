# Tutorial 4: Production Ready - FastAPI

Simple FastAPI deployment for Google ADK agents.

## Overview

Deploy an ADK agent as a REST API using FastAPI and Docker.

## Setup

```bash
cd 4-production-ready
uv sync
```

## Run Locally

```bash
uv run uvicorn app.main:app --reload --port 8080
```

Visit http://localhost:8080/docs to test the API.

## Test the API

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message": "Hello!"}'
```

## Test Streaming

```bash
curl -X POST http://localhost:8080/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"user_message": "Tell me a story"}'
```

## Docker

Build:
```bash
docker build -t adk-agent .
```

Run:
```bash
docker run -p 8080:8080 \
  -e GOOGLE_API_KEY=your_google_api_key \
  adk-agent
```

## API Endpoints

- `GET /health` - Health check
- `POST /chat` - Send message, get complete response
  - Request: `{"user_message": "your message"}`
  - Response: `{"response": "agent response"}`
- `POST /chat/stream` - Stream response chunks
  - Request: `{"user_message": "your message"}`
  - Response: NDJSON stream of `{"chunk": "..."}`
