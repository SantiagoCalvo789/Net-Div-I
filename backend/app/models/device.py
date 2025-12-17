from pydantic import BaseModel, Field
from pydantic.networks import IPvAnyAddress


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del dispositivo")
    ip_address: IPvAnyAddress = Field(..., description="IP del dispositivo (IPv4 o IPv6)")
    device_type: str = Field(..., min_length=1, max_length=50, description="Tipo: switch, router, ap, firewall, etc.")
    location: str = Field(..., min_length=1, max_length=100, description="Ubicación física o lógica")


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int