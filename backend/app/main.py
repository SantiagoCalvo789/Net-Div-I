from fastapi import FastAPI, HTTPException

from backend.app.core.db import get_conn
from backend.app.models.device import Device, DeviceCreate, DeviceUpdate
from psycopg.errors import UniqueViolation

app = FastAPI(title="Network Device Inventory API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/devices", response_model=list[Device])
def list_devices():
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, name, ip_address, device_type, location
            FROM devices
            ORDER BY id ASC
            """
        ).fetchall()

    return [
        Device(
            id=row[0],
            name=row[1],
            ip_address=row[2],
            device_type=row[3],
            location=row[4],
        )
        for row in rows
    ]


@app.get("/devices/{device_id}", response_model=Device)
def get_device(device_id: int):
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT id, name, ip_address, device_type, location
            FROM devices
            WHERE id = %s
            """,
            (device_id,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Device not found")

    return Device(
        id=row[0],
        name=row[1],
        ip_address=row[2],
        device_type=row[3],
        location=row[4],
    )


@app.post("/devices", response_model=Device, status_code=201)
def create_device(payload: DeviceCreate):
    try:
        with get_conn() as conn:
            row = conn.execute(
                """
                INSERT INTO devices (name, ip_address, device_type, location)
                VALUES (%s, %s, %s, %s)
                RETURNING id, name, ip_address, device_type, location
                """,
                (
                    payload.name,
                    str(payload.ip_address),
                    payload.device_type,
                    payload.location,
                ),
            ).fetchone()
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="ip_address already exists")


    return Device(
        id=row[0],
        name=row[1],
        ip_address=row[2],
        device_type=row[3],
        location=row[4],
    )


@app.put("/devices/{device_id}", response_model=Device)
def update_device(device_id: int, payload: DeviceUpdate):
    with get_conn() as conn:
        row = conn.execute(
            """
            UPDATE devices
            SET name = %s,
                ip_address = %s,
                device_type = %s,
                location = %s
            WHERE id = %s
            RETURNING id, name, ip_address, device_type, location
            """,
            (
                payload.name,
                payload.ip_address,
                payload.device_type,
                payload.location,
                device_id,
            ),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Device not found")

    return Device(
        id=row[0],
        name=row[1],
        ip_address=row[2],
        device_type=row[3],
        location=row[4],
    )


@app.delete("/devices/{device_id}", status_code=204)
def delete_device(device_id: int):
    with get_conn() as conn:
        row = conn.execute(
            """
            DELETE FROM devices
            WHERE id = %s
            RETURNING id
            """,
            (device_id,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Device not found")

    return None