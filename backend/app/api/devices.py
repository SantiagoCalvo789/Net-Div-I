from fastapi import APIRouter, HTTPException

from backend.app.models.device import Device, DeviceCreate, DeviceUpdate
from backend.app.services.devices_service import (
    create_device_db,
    delete_device_db,
    get_device_db,
    list_devices_db,
    update_device_db,
)

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", response_model=list[Device])
def list_devices():
    return list_devices_db()


@router.get("/{device_id}", response_model=Device)
def get_device(device_id: int):
    device = get_device_db(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("", response_model=Device, status_code=201)
def create_device(payload: DeviceCreate):
    # Esta función devuelve:
    # - Device si se creó
    # - "duplicate_ip" si ya existe
    result = create_device_db(payload)
    if result == "duplicate_ip":
        raise HTTPException(status_code=409, detail="ip_address already exists")
    return result


@router.put("/{device_id}", response_model=Device)
def update_device(device_id: int, payload: DeviceUpdate):
    device = update_device_db(device_id, payload)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.delete("/{device_id}", status_code=204)
def delete_device(device_id: int):
    ok = delete_device_db(device_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Device not found")
    return None