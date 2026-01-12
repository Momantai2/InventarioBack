from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any

@dataclass
class Equipment:
    serie: str
    modelo_id: int
    estado_id: int
    ubicacion_id: int
    proveedor_id: Optional[int] = None
    personal_usuario_id: Optional[int] = None
    specs: Dict[str, Any] = None
    observaciones: Optional[str] = None
    id: Optional[int] = None