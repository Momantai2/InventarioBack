from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from src.schemas.common import CommonBaseRead, CommonBaseCreate,CommonBaseUpdate,CommonBasePagedResponse

class GerenciaRead(CommonBaseRead):
    pass
GerenciaPagedResponse = CommonBasePagedResponse[GerenciaRead]
class GerenciaCreate(CommonBaseCreate):
    pass
class GerenciaUpdate(CommonBaseUpdate):
    pass
class AreaRead(CommonBaseRead):
    gerencias : Optional[GerenciaRead] = None
    
AreaPagedResponse = CommonBasePagedResponse[AreaRead]

class AreaCreate(CommonBaseCreate):
    gerencia_id: int
class AreaUpdate(CommonBaseUpdate):
    gerencia_id: Optional[int] = None

class DepartamentosRead(CommonBaseRead):
    pass
DepartamentoPagedResponse = CommonBasePagedResponse[DepartamentosRead]

class DepartamentosCreate(CommonBaseCreate):
    pass
class DepartamentosUpdate(CommonBaseUpdate):
    pass

class TiposLocalRead(CommonBaseRead):
    pass
TiposLocalPagedResponse = CommonBasePagedResponse[TiposLocalRead]

class TiposLocalCreate(CommonBaseCreate):
    pass
class TiposLocalUpdate(CommonBaseUpdate):
    pass


class SedesAgenciasRead(CommonBaseRead):
    departamentos: Optional[DepartamentosRead] = None
    tipos_local: Optional[TiposLocalRead] = None
    
SedesAgenciasPagedResponse = CommonBasePagedResponse[SedesAgenciasRead]

    
class SedesAgenciasCreate(CommonBaseCreate):
    departamento_id: int
    tipo_local_id: int
class SedesAgenciasUpdate(CommonBaseUpdate):
    departamento_id: Optional[int] = None
    tipo_local_id: Optional[int] = None

class UbicacionesDetalladasRead(BaseModel):
    id: int
    piso_oficina: str
    areas: Optional[AreaRead] = None
    sedes_agencias: Optional[SedesAgenciasRead] = None
    
    model_config = ConfigDict(from_attributes=True)
    
UbicacionesDetalladasPagedResponse = CommonBasePagedResponse[UbicacionesDetalladasRead]

class UbicacionesDetalladasCreate(BaseModel):
    area_id: int
    sede_id: int
    piso_oficina: str
    activo: bool = True

class UbicacionesDetalladaUpdate(BaseModel):
    area_id: Optional[int] = None
    sede_id: Optional[int] = None
    piso_oficina: Optional[str] = None
    activo: Optional[bool] = None



