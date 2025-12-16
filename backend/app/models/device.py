from pydantic import BaseModel, Field


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del dispositivo")
    ip_address: str = Field(..., min_length=7, max_length=45, description="IP del dispositivo")
    device_type: str = Field(..., min_length=1, max_length=50, description="Tipo: switch, router, ap, firewall, etc.")
    location: str = Field(..., min_length=1, max_length=100, description="Ubicación física o lógica")


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int