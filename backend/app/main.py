from fastapi import FastAPI

from backend.app.api.devices import router as devices_router

app = FastAPI(title="Network Device Inventory API")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(devices_router)