from fastapi import FastAPI

app = FastAPI(title="Organization Service")

@app.get("/health")
async def health():
    return {"status": 200, "message": "Running"}
