from fastapi import FastAPI
from pydantic import BaseModel
import os, httpx

app = FastAPI(title="pep")

class EvalRequest(BaseModel):
    user_id: str | None = None
    prompt: str
    sensitivity: str | None = None
    labels: list[str] = []

PDP_URL = os.getenv("PDP_URL", "http://aims:8080")

@app.get("/healthz")
async def healthz(): return {"status":"ok","service":"pep"}

@app.post("/v1/decide")
async def decide(req: EvalRequest):
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.post(f"{PDP_URL}/v1/pdp/decide", json=req.model_dump())
        r.raise_for_status()
        return r.json()
