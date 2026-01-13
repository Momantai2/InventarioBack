from pydantic import BaseModel
from typing import Optional

class CatalogBase(BaseModel):
    nombre: str

class CatalogCreate(CatalogBase):
    pass

class CatalogRead(CatalogBase):
    id: int
    
class ModelCreate(BaseModel):
    nombre: str
    marca_id: int
    tipo_equipo_id: int

class ModelRead(BaseModel):
    id: int
    nombre: str
    marca_id: int
    tipo_equipo_id: int
    # Estos campos contendrán los datos de las tablas relacionadas
    marcas: Optional[CatalogRead] = None
    tipos_equipo: Optional[CatalogRead] = None
    class Config:
        from_attributes = True