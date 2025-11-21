from fastapi import FastAPI
from .controllers import router as run_router

app = FastAPI(title="Alexandria")

app.include_router(run_router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Alexandria Backend running"}
