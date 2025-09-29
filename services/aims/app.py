from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="aims")

EVIDENCE: list[dict] = []
RULES = {"deny":["password","ssn","credit card"], "mask":["email@","@company.com"]}

class PDPInput(BaseModel):
    user_id: str | None = None
    prompt: str
    sensitivity: str | None = None
    labels: list[str] = []

@app.get("/healthz")
async def healthz(): return {"status":"ok","service":"aims"}

@app.post("/v1/pdp/decide")
async def pdp_decide(inp: PDPInput):
    p = inp.prompt.lower()
    if (inp.sensitivity or "").lower() in {"confidential","restricted"}:
        for kw in RULES["deny"]:
            if kw in p: return {"decision":"deny","reason":f"Found '{kw}'"}
    mask_terms = [kw for kw in RULES["mask"] if kw in inp.prompt]
    if mask_terms: return {"decision":"modify","mask_terms":mask_terms,"reason":"masked low-risk ids"}
    return {"decision":"allow","reason":"default allow"}

class Evidence(BaseModel):
    kind: str
    decision: str | None = None

@app.post("/v1/evidence")
async def add_evidence(ev: Evidence):
    EVIDENCE.append(ev.model_dump())
    return {"ok": True, "count": len(EVIDENCE)}

@app.get("/v1/evidence")
async def list_ev(): return {"items": EVIDENCE[-100:]}
