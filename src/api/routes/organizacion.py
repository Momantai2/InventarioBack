from fastapi import APIRouter, Depends, Query, status
from typing import Optional
# Importamos también el PagedResponse y los modelos de lectura
from src.schemas.organization import (
    GerenciaRead, 
    GerenciaCreate, 
    GerenciaUpdate, 
    GerenciaPagedResponse,
    AreaRead, AreaCreate, AreaUpdate, AreaPagedResponse,
    DepartamentosRead,DepartamentosCreate,DepartamentosUpdate,DepartamentoPagedResponse,
    TiposLocalRead,TiposLocalCreate,TiposLocalUpdate,TiposLocalPagedResponse,
    SedesAgenciasRead,SedesAgenciasCreate,SedesAgenciasUpdate,SedesAgenciasPagedResponse,
    UbicacionesDetalladasRead,UbicacionesDetalladasCreate,UbicacionesDetalladaUpdate,UbicacionesDetalladasPagedResponse
)
from src.application.services.organization_service import OrganizationService
from src.infrastructure.repositories.organization_repository_impl import OrganizationRepositoryImpl

router = APIRouter(prefix="/organizacion", tags=["Organización"])

def get_organization_service():
    repository = OrganizationRepositoryImpl()
    return OrganizationService(repository)

# --- RUTAS DE GERENCIAS ---

@router.get("/gerencias", response_model=GerenciaPagedResponse) # <--- AÑADIDO
async def listar_gerencias(
    query: Optional[str] = Query(None, description="Buscar por nombre"),
    page: int = Query(1, ge=1), # Añadimos ge=1 para validar que sea >= 1
    page_size: int = Query(20, ge=1, le=100), # Añadimos límites
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.get_gerencias(query=query, page=page, page_size=page_size)

@router.post("/gerencias", response_model=GerenciaRead, status_code=status.HTTP_201_CREATED) # <--- AÑADIDO
async def crear_gerencia(
    data: GerenciaCreate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.create_gerencia(data)

@router.patch("/gerencias/{gerencia_id}", response_model=GerenciaRead) # <--- AÑADIDO
async def actualizar_gerencia(
    gerencia_id: int,
    data: GerenciaUpdate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.update_gerencia(gerencia_id, data)

@router.delete("/gerencias/{gerencia_id}") 
async def eliminar_gerencia(
    gerencia_id: int,
    service: OrganizationService = Depends(get_organization_service)
):

    return await service.delete_gerencia(gerencia_id)

# --- RUTAS DE ÁREAS ---

@router.get("/areas", response_model=AreaPagedResponse)
async def listar_areas(
    query: Optional[str] = Query(None, description="Buscar por nombre de área"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: OrganizationService = Depends(get_organization_service)
):
    """Obtiene áreas con su gerencia vinculada."""
    return await service.get_areas(query=query, page=page, page_size=page_size)

@router.post("/areas", response_model=AreaRead, status_code=status.HTTP_201_CREATED)
async def crear_area(
    data: AreaCreate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.create_area(data)

@router.patch("/areas/{area_id}", response_model=AreaRead)
async def actualizar_area(
    area_id: int,
    data: AreaUpdate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.update_area(area_id, data)

@router.delete("/areas/{area_id}")
async def eliminar_area(
    area_id: int,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.delete_area(area_id)

# --- RUTAS DE DEPARTAMENTOS ---

@router.get("/departamentos", response_model=DepartamentoPagedResponse) 
async def listar_departamentos(
    query: Optional[str] = Query(None, description="Buscar por nombre"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(20, ge=1, le=100), 
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.get_departamentos(query=query, page=page, page_size=page_size)

@router.post("/departamentos", response_model=DepartamentosRead, status_code=status.HTTP_201_CREATED) 
async def crear_departamento(
    data: DepartamentosCreate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.create_departamento(data)

@router.patch("/departamentos/{departamento_id}", response_model=DepartamentosRead) 
async def actualizar_departamento(
    departamento_id: int,
    data: DepartamentosUpdate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.update_departamento(departamento_id, data)

@router.delete("/departamentos/{departamento_id}") 
async def eliminar_departamento(
    departamento_id: int,
    service: OrganizationService = Depends(get_organization_service)
):

    return await service.delete_departamento(departamento_id)

# --- RUTAS DE TIPOS LOCAL ---

@router.get("/tipo_local", response_model=TiposLocalPagedResponse) 
async def listar_tipos_local(
    query: Optional[str] = Query(None, description="Buscar por nombre"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(20, ge=1, le=100), 
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.get_tipos_local(query=query, page=page, page_size=page_size)

@router.post("/tipo_local", response_model=TiposLocalRead, status_code=status.HTTP_201_CREATED) 
async def crear_tipo_local(
    data: TiposLocalCreate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.create_tipos_local(data)

@router.patch("/tipo_local/{tipos_local_id}", response_model=TiposLocalRead) 
async def actualizar_tipo_local(
    tipos_local_id: int,
    data: TiposLocalUpdate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.update_tipos_local(tipos_local_id, data)

@router.delete("/tipo_local/{tipos_local_id}") 
async def eliminar_tipo_local(
    tipos_local_id: int,
    service: OrganizationService = Depends(get_organization_service)
):

    return await service.delete_tipos_local(tipos_local_id)

@router.get("/sedes_agencias", response_model=SedesAgenciasPagedResponse)
async def listar_sedes_agencias(
    query: Optional[str] = Query(None, description="Buscar por nombre de sede"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.get_sedes_agencias(query=query, page=page, page_size=page_size)

@router.post("/sedes_agencias", response_model=SedesAgenciasRead, status_code=status.HTTP_201_CREATED)
async def crear_sede_agencia(
    data: SedesAgenciasCreate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.create_sede_agencia(data)

@router.patch("/sedes_agencias/{sede_id}", response_model=SedesAgenciasRead)
async def actualizar_sede_agencia(
    sede_id: int,
    data: SedesAgenciasUpdate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.update_sede_agencia(sede_id, data)

@router.delete("/sedes_agencias/{sede_id}")
async def eliminar_sede_agencia(
    sede_id: int,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.delete_sede_agencia(sede_id)

@router.get("/ubicaciones_detalladas", response_model=UbicacionesDetalladasPagedResponse)
async def listar_ubicaciones(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.get_ubicaciones_detalladas(page=page, page_size=page_size)

@router.post("/ubicaciones_detalladas", response_model=UbicacionesDetalladasRead, status_code=status.HTTP_201_CREATED)
async def crear_ubicacion(
    data: UbicacionesDetalladasCreate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.create_ubicacion_detallada(data)

@router.patch("/ubicaciones_detalladas/{ubicacion_id}", response_model=UbicacionesDetalladasRead)
async def actualizar_ubicacion(
    ubicacion_id: int,
    data: UbicacionesDetalladaUpdate,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.update_ubicacion_detallada(ubicacion_id, data)

@router.delete("/ubicaciones_detalladas/{ubicacion_id}")
async def eliminar_ubicacion(
    ubicacion_id: int,
    service: OrganizationService = Depends(get_organization_service)
):
    return await service.delete_ubicacion_detallada(ubicacion_id)


