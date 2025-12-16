from typing import Dict
from backend.app.models.device import Device

devices_db: Dict[int, Device] = {}
next_id: int = 1