from fastapi import FastAPI

app = FastAPI(title="Auth Service")

@app.get("/health")
async def health():
    return {"status": "ok"}
