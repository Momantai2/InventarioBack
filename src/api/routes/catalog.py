from fastapi import APIRouter, Depends, Query, status
from src.application.services.catalog_service import CatalogService
from src.infrastructure.repositories.catalog_repository_impl import CatalogRepositoryImpl
from src.schemas.catalog import MarcaCreate,MarcaPagedResponse,MarcaRead,MarcaUpdate, TiposEquipoCreate,TiposEquipoPagedResponse,TiposEquipoRead,TiposEquipoUpdate,EstadoCreate,EstadoPagedResponse,EstadoRead,EstadoUpdate,ModelosCreate,ModelosPagedResponse,ModelosRead,ModelosUpdate
from typing import Optional
from src.application.services.catalog_service import CatalogService

router = APIRouter(prefix="/catalogos", tags=["Catalogos"])

def get_catalogos_service():
    repository = CatalogRepositoryImpl()
    return CatalogService(repository)


#MARCAS
@router.get("/marcas", response_model=MarcaPagedResponse) 
async def listar_marcas(
    query: Optional[str] = Query(None, description="Buscar por nombre"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(20, ge=1, le=100), 
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.get_marcas(query=query, page=page, page_size=page_size)

@router.post("/marcas", response_model=MarcaRead, status_code=status.HTTP_201_CREATED) 
async def crear_gerencia(
    data: MarcaCreate,
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.create_marca(data)

@router.patch("/marcas/{marca_id}", response_model=MarcaRead) 
async def actualizar_marcas(
    marca_id: int,
    data: MarcaUpdate,
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.update_marca(marca_id, data)

@router.delete("/marcas/{marca_id}") 
async def eliminar_marca(
    marca_id: int,
    service: CatalogService = Depends(get_catalogos_service)
):

    return await service.delete_marca(marca_id)

#TIPOS EQUIPOS

@router.get("/tipos_equipos", response_model=TiposEquipoPagedResponse) 
async def listar_tipos_equipo(
    query: Optional[str] = Query(None, description="Buscar por nombre"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(20, ge=1, le=100), 
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.get_tipos_equipo(query=query, page=page, page_size=page_size)

@router.post("/tipos_equipos", response_model=TiposEquipoRead, status_code=status.HTTP_201_CREATED) 
async def crear_tipo_equipo(
    data: TiposEquipoCreate,
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.create_tipo_equipo(data)

@router.patch("/tipos_equipos/{tipos_equipo_id}", response_model=TiposEquipoRead) 
async def actualizar_tipo_equipo(
    tipos_equipo_id: int,
    data: TiposEquipoUpdate,
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.update_tipos_equipo(tipos_equipo_id, data)

@router.delete("/tipos_equipos/{tipos_equipo_id}") 
async def eliminar_tipo_equipo(
    tipos_equipo_id: int,
    service: CatalogService = Depends(get_catalogos_service)
):

    return await service.delete_tipos_equipo(tipos_equipo_id)

#ESTADOS

@router.get("/estados", response_model=EstadoPagedResponse) 
async def listar_estados(
    query: Optional[str] = Query(None, description="Buscar por nombre"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(20, ge=1, le=100), 
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.get_estados(query=query, page=page, page_size=page_size)

@router.post("/estados", response_model=EstadoRead, status_code=status.HTTP_201_CREATED) 
async def crear_estado(
    data: EstadoCreate,
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.create_estado(data)

@router.patch("/estados/{estado_id}", response_model=EstadoRead) 
async def actualizar_marcas(
    estado_id: int,
    data: EstadoUpdate,
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.update_estado(estado_id, data)

@router.delete("/estados/{estado_id}") 
async def eliminar_estado(
    estado_id: int,
    service: CatalogService = Depends(get_catalogos_service)
):

    return await service.delete_estado(estado_id)

#MODELOS 

@router.get("/modelos", response_model=ModelosPagedResponse) 
async def listar_modelos(
    query: Optional[str] = Query(None, description="Buscar por nombre"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(20, ge=1, le=100), 
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.get_modelos(query=query, page=page, page_size=page_size)

@router.post("/modelos", response_model=ModelosRead, status_code=status.HTTP_201_CREATED) 
async def crear_modelo(
    data: ModelosCreate,
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.create_modelo(data)

@router.patch("/modelos/{modelo_id}", response_model=ModelosRead) 
async def actualizar_modelo(
    modelo_id: int,
    data: ModelosUpdate,
    service: CatalogService = Depends(get_catalogos_service)
):
    return await service.update_modelo(modelo_id, data)

@router.delete("/modelos/{modelo_id}") 
async def eliminar_modelo(
    modelo_id: int,
    service: CatalogService = Depends(get_catalogos_service)
):

    return await service.delete_modelo(modelo_id)
