from fastapi import FastAPI
from pydantic import BaseModel
import os, httpx

app = FastAPI(title="rag")

class RAGQuery(BaseModel):
    prompt: str
    labels: list[str] = []

TOOLS_URL  = os.getenv("TOOLS_URL",  "http://tools:8080")
MODELS_URL = os.getenv("MODELS_URL", "http://models:8080")

@app.get("/healthz")
async def healthz(): return {"status":"ok","service":"rag"}

@app.post("/v1/answer")
async def answer(q: RAGQuery):
    async with httpx.AsyncClient(timeout=10) as c:
        t = await c.post(f"{TOOLS_URL}/v1/toolcall", json={"prompt": q.prompt})
        t.raise_for_status()
        ctx = t.json().get("context","")
        m = await c.post(f"{MODELS_URL}/v1/generate", json={"prompt": q.prompt, "context": ctx})
        m.raise_for_status()
        out = m.json()
    return {"answer": out.get("text"), "used_context": ctx}
