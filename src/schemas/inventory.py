from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Any, List
from datetime import date
from src.schemas.common import AuditoriaBase, CommonBasePagedResponse

class EquipmentBase(BaseModel):
    serie: str = Field(..., min_length=3)
    modelo_id: int
    estado_id: int
    ubicacion_id: int
    proveedor_id: Optional[int] = None
    personal_usuario_id: Optional[int] = None
    specs: dict[str, Any] = {}
    observaciones: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(BaseModel):
    serie: Optional[str] = None
    modelo_id: Optional[int] = None
    estado_id: Optional[int] = None
    ubicacion_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    personal_usuario_id: Optional[int] = None
    specs: Optional[dict[str, Any]] = None
    observaciones: Optional[str] = None

class EquipmentRead(EquipmentBase, AuditoriaBase):
    id: int
    # Campos virtuales que vienen del JOIN
    modelos: Optional[dict] = None
    estados: Optional[dict] = None
    ubicaciones_detalladas: Optional[dict] = None
    personas: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)

EquipmentPagedResponse = CommonBasePagedResponse[EquipmentRead]

class ProveedorRentingCreate(BaseModel):
    nombre: str
    # Usar Optional y None como default para que FastAPI no obligue a enviarlos
    fecha_inicio_contrato: Optional[date] = None
    fecha_vencimiento_contrato: Optional[date] = None

class ProveedorRentingRead(ProveedorRentingCreate):
    id: int


