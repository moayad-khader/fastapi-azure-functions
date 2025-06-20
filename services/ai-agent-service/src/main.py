from fastapi import FastAPI

app = FastAPI(title="Ai Agent Service")

@app.get("/health")
async def health():
    return {"status": "ok"}
