from pydantic import BaseModel
from typing import Optional

class PersonBase(BaseModel):
    dni: str
    nombre_completo: str
    area_id: int
    activo: bool = True

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    dni: Optional[str] = None
    nombre_completo: Optional[str] = None
    area_id: Optional[int] = None
    activo: Optional[bool] = None

class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True