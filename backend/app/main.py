from fastapi import FastAPI

app = FastAPI(title="Network Device Inventory API")


@app.get("/health")
def health():
    return {"status": "ok"}