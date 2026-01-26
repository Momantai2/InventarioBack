from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from src.schemas.common import CommonBaseRead, CommonBaseCreate,CommonBaseUpdate,CommonBasePagedResponse,AuditoriaBase

class MarcaRead(CommonBaseRead):
    pass
MarcaPagedResponse = CommonBasePagedResponse[MarcaRead]
class MarcaCreate(CommonBaseCreate):
    pass
class MarcaUpdate(CommonBaseUpdate):
    pass

class TiposEquipoRead(CommonBaseRead):
    pass
TiposEquipoPagedResponse = CommonBasePagedResponse[TiposEquipoRead]
class TiposEquipoCreate(CommonBaseCreate):
    pass
class TiposEquipoUpdate(CommonBaseUpdate):
    pass

class EstadoRead(CommonBaseRead):
    pass
EstadoPagedResponse = CommonBasePagedResponse[EstadoRead]
class EstadoCreate(CommonBaseCreate):
    pass
class EstadoUpdate(CommonBaseUpdate):
    pass

class ModelosRead(CommonBaseRead):
    marcas: Optional[MarcaRead] = None
    tipos_equipo: Optional[TiposEquipoRead] = None
    
    model_config = ConfigDict(from_attributes=True)

ModelosPagedResponse = CommonBasePagedResponse[ModelosRead]
class ModelosCreate(CommonBaseCreate):
    marca_id: int
    tipo_equipo_id: int

class ModelosUpdate(CommonBaseUpdate):
    marca_id: Optional[int] = None
    tipo_equipo_id: Optional[int] = None