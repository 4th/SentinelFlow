from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(title="models")
class GenReq(BaseModel):
    prompt: str
    context: str = ""
@app.get("/healthz")
async def healthz(): return {"status":"ok","service":"models"}
@app.post("/v1/generate")
async def generate(req: GenReq):
    return {"text": f"Echo: {req.prompt} | ctx bytes: {len(req.context)}"}
