from pydantic import BaseModel, ConfigDict
from typing import Optional,Any
from datetime import date

class EquipmentCreate(BaseModel):
    serie: str
    modelo_id: int
    estado_id: int
    ubicacion_id: int
    proveedor_id: Optional[int] = None
    personal_usuario_id: Optional[int] = None
    specs: dict[str, Any] = {}
    observaciones: Optional[str] = None


class ProveedorRentingCreate(BaseModel):
    nombre: str
    # Usar Optional y None como default para que FastAPI no obligue a enviarlos
    fecha_inicio_contrato: Optional[date] = None
    fecha_vencimiento_contrato: Optional[date] = None

class ProveedorRentingRead(ProveedorRentingCreate):
    id: int
    # Para compatibilidad con los datos que vienen de Supabase/PostgreSQL
    model_config = ConfigDict(from_attributes=True)

class BulkAssignRequest(BaseModel):
    equipment_ids: list[int]
    person_id: int
    
