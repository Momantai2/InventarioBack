from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class TunedModel(BaseModel):
    """Configuración base para permitir la conversión de objetos de base de datos."""
    model_config = ConfigDict(from_attributes=True)

class HistorialAsignacionesBase(BaseModel):
    """Campos comunes para la gestión de asignaciones."""
    equipo_id: int
    persona_id: int
    tipo_movimiento_id: int
    # Usamos default_factory para que se asigne la hora exacta al crear el objeto
    fecha_inicio: datetime = Field(default_factory=datetime.now)
    fecha_fin: Optional[datetime] = None
    observaciones: Optional[str] = Field(None, max_length=150)

class HistorialAsignacionesCreate(HistorialAsignacionesBase):
    """Esquema utilizado para recibir nuevas asignaciones desde el frontend."""
    # No pedimos el ID porque es autoincremental en Supabase
    pass

class HistorialAsignacionesRead(HistorialAsignacionesBase, TunedModel):
    """Esquema para devolver datos al frontend con información de tablas relacionadas."""
    id: int
    # Estos campos almacenan los diccionarios que vienen de los JOINs en Supabase
    equipos: Optional[dict] = None
    personas: Optional[dict] = None
    tipos_movimiento_historial: Optional[dict] = None
    
class BulkAssignRequest(BaseModel):
    """Esquema para asignar múltiples equipos a una sola persona."""
    equipment_ids: list[int]
    person_id: int
    # Podrías agregar tipo_movimiento_id aquí si quieres especificarlo en lote