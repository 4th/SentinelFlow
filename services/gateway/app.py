from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, httpx

app = FastAPI(title="gateway")

class Query(BaseModel):
    user_id: str | None = None
    prompt: str
    sensitivity: str | None = None
    labels: list[str] = []

PEP_URL  = os.getenv("PEP_URL",  "http://pep:8080")
RAG_URL  = os.getenv("RAG_URL",  "http://rag:8080")
AIMS_URL = os.getenv("AIMS_URL", "http://aims:8080")

@app.get("/healthz")
async def healthz(): return {"status":"ok","service":"gateway","version":os.getenv("VERSION","dev")}

@app.post("/v1/route")
async def route(q: Query):
    # 1) ask PEP
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            d = await c.post(f"{PEP_URL}/v1/decide", json=q.model_dump())
            d.raise_for_status()
            decision = d.json()
    except Exception as e:
        raise HTTPException(502, f"PEP unavailable: {e}")

    if decision.get("decision") == "deny":
        return {"allowed": False, "reason": decision.get("reason")}

    # 2) apply modify/masking if any
    prompt = q.prompt
    for t in decision.get("mask_terms", []):
        prompt = prompt.replace(t, "[REDACTED]")

    # 3) call RAG
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(f"{RAG_URL}/v1/answer", json={"prompt": prompt, "labels": q.labels})
            r.raise_for_status()
            payload = r.json()
    except Exception as e:
        raise HTTPException(502, f"RAG unavailable: {e}")

    # 4) non-blocking evidence
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            await c.post(f"{AIMS_URL}/v1/evidence", json={"kind":"gateway_log","decision":decision.get("decision")})
    except Exception:
        pass

    return {"allowed": True, "result": payload}
