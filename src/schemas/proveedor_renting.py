from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import date
from src.schemas.common import AuditoriaBase

class ProveedorRentingBase(AuditoriaBase):
    nombre: str
    fecha_inicio_contrato: Optional[date] = None
    fecha_vencimiento_contrato: Optional[date] = None

class ProveedorRentingCreate(ProveedorRentingBase):
    pass

class ProveedorRentingRead(ProveedorRentingBase):
    id: int

    # Este decorador soluciona el error de "Object of type date is not JSON serializable"
    @field_serializer('fecha_inicio_contrato', 'fecha_vencimiento_contrato')
    def serialize_date(self, dt: date, _info):
        return dt.isoformat() if dt else None

    class Config:
        from_attributes = True