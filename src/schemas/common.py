from pydantic import BaseModel, ConfigDict, field_serializer
from typing import Optional, List, TypeVar, Generic 
from datetime import datetime
import pytz

T = TypeVar("T")

class AuditoriaBase(BaseModel):
    activo: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_serializer('created_at', 'updated_at')
    def serialize_dt(self, dt: datetime, _info):
        if dt is None:
            return None
        
        peru_tz = pytz.timezone('America/Lima')
        
        return dt.astimezone(peru_tz).isoformat()
    
class CommonBaseRead(AuditoriaBase):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class CommonBaseCreate(BaseModel):
    nombre: str
    activo: bool = True

class CommonBaseUpdate(BaseModel):
    nombre: Optional[str] = None
    activo: Optional[bool] = None

class CommonBasePagedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int


    