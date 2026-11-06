# A copy of the routing skeleton of src/api-service/api/service.py:12-50 at 3ecef56 (the two routes
# "/" and "/status", the inner api_app mounted under ROOT_PATH in an outer app), without the routers,
# which import the model, Chroma and Vertex AI. Used by fastapi.sh.
import os
from fastapi import FastAPI

ROOT_PATH = os.getenv("ROOT_PATH", "")
api_app = FastAPI(title="API Server", description="API Server", version="v1")

@api_app.get("/")
async def get_index():
    return {"message": "Welcome to AC215"}

@api_app.get("/status")
async def get_api_status():
    return {"version": "3.0"}

app = FastAPI(title="API Server", description="API Server", version="v1")
app.mount(ROOT_PATH, api_app)
