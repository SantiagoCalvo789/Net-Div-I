from fastapi import FastAPI, HTTPException
from backend.app.core.memory_store import devices_db
from backend.app.models.device import Device, DeviceCreate, DeviceUpdate

app = FastAPI(title="Network Device Inventory API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/devices", response_model=list[Device])
def list_devices():
    return list(devices_db.values())


@app.get("/devices/{device_id}", response_model=Device)
def get_device(device_id: int):
    device = devices_db.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@app.post("/devices", response_model=Device, status_code=201)
def create_device(payload: DeviceCreate):
    # Generar ID manualmente (simulación de autoincrement)
    new_id = (max(devices_db.keys()) + 1) if devices_db else 1
    device = Device(id=new_id, **payload.model_dump())
    devices_db[new_id] = device
    return device


@app.put("/devices/{device_id}", response_model=Device)
def update_device(device_id: int, payload: DeviceUpdate):
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    updated = Device(id=device_id, **payload.model_dump())
    devices_db[device_id] = updated
    return updated


@app.delete("/devices/{device_id}", status_code=204)
def delete_device(device_id: int):
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    del devices_db[device_id]
    return None