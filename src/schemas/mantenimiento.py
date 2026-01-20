from pydantic import BaseModel, Field
from datetime import  datetime,date
from typing import Optional

class MantenimientoBase(BaseModel):
    equipo_id: int
    tipos_mantenimiento_id: int
    descripcion: Optional[str] = None
    costo: float = Field(default=0.0, ge=0)
    fecha_inicio: date = Field(default_factory=datetime.today)
    fecha_fin: Optional[date] = None

class MantenimientoCreate(MantenimientoBase):
    """Esquema para registrar un nuevo ingreso a taller."""
    pass

class MantenimientoUpdate(BaseModel):
    """Esquema para finalizar un mantenimiento o editar detalles."""
    descripcion: Optional[str] = None
    costo: Optional[float] = None
    fecha_fin: Optional[date] = None

class MantenimientoRead(MantenimientoBase):
    """Esquema para devolver datos al frontend (incluye ID)."""
    id: int
    equipo_serie: Optional[str] = "N/A"
    # Opcional: Para incluir el nombre del tipo en el listado
    tipos_mantenimiento: Optional[dict] = None 
    equipos: Optional[dict] = None
    class Config:
        # Esto permite que Pydantic lea diccionarios o objetos y 
        # convierta fechas a texto automáticamente
        from_attributes = True 
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
        }
 #TIPOS MANTENIMIENTO
 
class TipoMantenimientoBase(BaseModel):
    # El nombre es obligatorio y único según tu esquema
    nombre: str = Field(..., min_length=1, max_length=100, example="PREVENTIVO")

class TipoMantenimientoCreate(TipoMantenimientoBase):
    """Esquema para creación (POST)"""
    pass

class TipoMantenimientoUpdate(BaseModel):
    """Esquema para actualización parcial (PATCH)"""
    nombre: Optional[str] = None

class TipoMantenimientoRead(TipoMantenimientoBase):
    """Esquema para lectura (GET)"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True