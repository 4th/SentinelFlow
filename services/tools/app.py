from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(title="tools")
class ToolReq(BaseModel): prompt: str
@app.get("/healthz")
async def healthz(): return {"status":"ok","service":"tools"}
@app.post("/v1/toolcall")
async def toolcall(req: ToolReq):
    return {"context": f"[ctx for: {req.prompt[:32]}...]"}
