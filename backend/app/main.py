from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.devices import router as devices_router

app = FastAPI(title="Network Device Inventory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(devices_router)