from typing import Literal

from psycopg.errors import UniqueViolation

from backend.app.core.db import get_conn
from backend.app.models.device import Device, DeviceCreate, DeviceUpdate


def _row_to_device(row) -> Device:
    return Device(
        id=row[0],
        name=row[1],
        ip_address=row[2],
        device_type=row[3],
        location=row[4],
    )


def list_devices_db() -> list[Device]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, name, ip_address, device_type, location
            FROM devices
            ORDER BY id ASC
            """
        ).fetchall()

    return [_row_to_device(r) for r in rows]


def get_device_db(device_id: int) -> Device | None:
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
        return None
    return _row_to_device(row)


def create_device_db(payload: DeviceCreate) -> Device | Literal["duplicate_ip"]:
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
        return "duplicate_ip"

    return _row_to_device(row)


def update_device_db(device_id: int, payload: DeviceUpdate) -> Device | None:
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
                str(payload.ip_address),
                payload.device_type,
                payload.location,
                device_id,
            ),
        ).fetchone()

    if not row:
        return None
    return _row_to_device(row)


def delete_device_db(device_id: int) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            """
            DELETE FROM devices
            WHERE id = %s
            RETURNING id
            """,
            (device_id,),
        ).fetchone()

    return row is not None