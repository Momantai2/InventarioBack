from pydantic import BaseModel
from typing import Optional, Dict, Any

class EquipmentCreate(BaseModel):
    serie: str
    modelo_id: int
    estado_id: int
    ubicacion_id: int
    proveedor_id: Optional[int] = None
    personal_usuario_id: Optional[int] = None
    specs: Dict[str, Any] = {}
    observaciones: Optional[str] = None