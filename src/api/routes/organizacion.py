from fastapi import APIRouter, Depends
from src.application.services.organization_service import OrganizationService
from src.infrastructure.repositories.organization_repository_impl import OrganizationRepositoryImpl
from src.schemas.organization import DepartamentoRead,UbicacionDetalladaCreate,SedeRead,SedeCreate,TipoLocalRead,TipoLocalCreate

router = APIRouter(tags=["Organización"])

def get_org_service():
    return OrganizationService(OrganizationRepositoryImpl())

@router.get("/organizacion/gerencias")
async def list_gerencias(service: OrganizationService = Depends(get_org_service)):
    return await service.get_all_gerencias()

@router.get("/organizacion/areas")
async def list_areas(service: OrganizationService = Depends(get_org_service)):
    return await service.get_all_areas()

@router.get("/organizacion/ubicaciones_detalladas")
async def list_ubicaciones(service: OrganizationService = Depends(get_org_service)):
    return await service.get_ubicaciones_detalladas()

@router.post("/organizacion/ubicaciones_detalladas")
async def create_ubicacion(data: UbicacionDetalladaCreate, service: OrganizationService = Depends(get_org_service)):
    # Convertimos a dict y pasamos al servicio
    return await service.create_ubicacion_detallada(data.model_dump())

@router.delete("/organizacion/ubicaciones_detalladas/{id}")
async def delete_ubicacion(id: int, service: OrganizationService = Depends(get_org_service)):
    return await service.delete_ubicacion(id)

# --- DEPARTAMENTOS ---
@router.get("/organizacion/departamentos", response_model=list[DepartamentoRead])
async def list_deps(service: OrganizationService = Depends(get_org_service)):
    return await service.get_departamentos()

# --- TIPOS DE LOCAL ---
@router.get("/organizacion/tipos_local", response_model=list[TipoLocalRead])
async def list_tipos_l(service: OrganizationService = Depends(get_org_service)):
    return await service.get_tipos_local()

# --- SEDES AGENCIAS ---
@router.get("/organizacion/sedes_agencias", response_model=list[SedeRead])
async def list_sedes(service: OrganizationService = Depends(get_org_service)):
    return await service.get_sedes()

@router.post("/organizacion/sedes_agencias", response_model=SedeRead)
async def add_sede(data: SedeCreate, service: OrganizationService = Depends(get_org_service)):
    return await service.create_sede(data.model_dump())