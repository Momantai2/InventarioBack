from pydantic import BaseModel
from typing import Optional, List

# --- Estructura Organizacional ---
class GerenciaRead(BaseModel):
    id: int
    nombre: str

class AreaCreate(BaseModel):
    nombre: str
    gerencia_id: int

class AreaRead(BaseModel):
    id: int
    nombre: str
    gerencia_id: int
    gerencias: Optional[GerenciaRead] = None # Relación anidada

# --- Estructura Física (Ubicaciones) ---
class DepartamentoRead(BaseModel):
    id: int
    nombre: str

class TipoLocalRead(BaseModel):
    id: int
    nombre: str

class SedeCreate(BaseModel):
    nombre: str
    departamento_id: int
    tipo_local_id: int

class SedeRead(BaseModel):
    id: int
    nombre: str
    departamento_id: int
    tipo_local_id: int
    departamentos: Optional[DepartamentoRead] = None
    tipos_local: Optional[TipoLocalRead] = None
    
class CatalogBase(BaseModel):
    nombre: str

class GerenciaCreate(CatalogBase): pass
class DepartamentoCreate(CatalogBase): pass
class TipoLocalCreate(CatalogBase): pass

# --- Ubicaciones Detalladas ---

class UbicacionDetalladaCreate(BaseModel):
    area_id: int
    sede_id: int
    piso_oficina: str

class UbicacionDetalladaRead(BaseModel):
    id: int
    area_id: int
    sede_id: int
    piso_oficina: str
    # Relaciones anidadas para mostrar en el frontend
    areas: Optional[AreaRead] = None
    sedes_agencias: Optional[SedeRead] = None

    class Config:
        from_attributes = True