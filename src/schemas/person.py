from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from src.schemas.common import AuditoriaBase,CommonBasePagedResponse
from src.schemas.organization import AreaRead


class PersonasRead(AuditoriaBase):
    id: int
    dni: str
    nombre_completo: str
    area_id: int
    activo: bool = True
    jefe_area: bool = True
    areas: Optional[AreaRead] = None

    model_config = ConfigDict(from_attributes=True)
    
PersonaPagedResponse = CommonBasePagedResponse[PersonasRead]

class PersonasCreate(BaseModel):
    dni: str
    nombre_completo: str
    area_id: int
    activo: bool = True
    jefe_area: bool = True
    activo: bool = True

class PersonasUpdate(BaseModel):
    dni: Optional[str] = None
    nombre_completo: Optional[str] = None
    area_id: Optional[int] = None
    activo: Optional[bool] = None
    jefe_area: Optional[bool] = None
    activo: Optional[bool] = None

    