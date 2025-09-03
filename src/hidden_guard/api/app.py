from __future__ import annotations
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import tempfile, os
from ..pipeline import HiddenGuardPipeline

app = FastAPI(title="HiddenGuard API", version="0.1.0")
pipeline = HiddenGuardPipeline()

@app.post("/scan")
async def scan(image: UploadFile = File(...), text: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[-1]) as tmp:
        content = await image.read()
        tmp.write(content)
        tmp_path = tmp.name
    try:
        out = pipeline.scan(tmp_path, text)
        return JSONResponse(out)
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

@app.get("/health")
async def health():
    return {"status": "ok"}
