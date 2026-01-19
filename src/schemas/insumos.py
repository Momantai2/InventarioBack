from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


#TABLA INSUMO
# Esquema base con campos comunes
class InsumoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    tipo_equipo_id: Optional[int] = None
    stock_minimo: int = 5
    stock_actual: int = 0

# Para crear: no pedimos ID porque lo genera la DB
class InsumoCreate(InsumoBase):
    pass

# Para leer: incluye el ID y datos de relaciones
class InsumoRead(InsumoBase, TunedModel):
    id: int
    tipos_equipo: Optional[dict] = None # Para el nombre de la categoría

class MovimientoInsumoCreate(BaseModel):
    insumo_id: int
    cantidad: int  
    motivo: str = Field(..., max_length=255)
    personal_id: Optional[int] = None

#TABLA MOVIMIENTO INSUMO

class InsumoMovimientoBase(BaseModel):
    insumo_id: Optional[int] = None
    personal_id: Optional[int] = None
    cantidad: int = 0
    fecha: datetime 
    motivo: str = Field(..., min_length=1, max_length=150)

class Insumo_Movimiento_Read(TunedModel):
    id: int
    insumo_id: int
    personal_id: Optional[int]
    cantidad: int
    fecha: datetime
    motivo: str
    # Para capturar los nombres de los joins
    insumos: Optional[dict] = None
    personas: Optional[dict] = None

class Insumo_MovimientoCreate(MovimientoInsumoCreate):
    pass


