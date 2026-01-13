from fastapi import APIRouter, Depends
from src.application.services.catalog_service import CatalogService
from src.infrastructure.repositories.catalog_repository_impl import CatalogRepositoryImpl
from src.schemas.catalog import CatalogCreate, ModelCreate,CatalogRead

router = APIRouter(tags=["Catálogos"])

def get_catalog_service():
    return CatalogService(CatalogRepositoryImpl())

# Endpoints de Marcas
@router.get("/catalogs/marcas")
async def list_marcas(service: CatalogService = Depends(get_catalog_service)):
    return await service.get_marcas()

@router.post("/catalogs/marcas")
async def add_marca(data: CatalogCreate, service: CatalogService = Depends(get_catalog_service)):
    return await service.create_marca(data.model_dump())

# Endpoints de Modelos
@router.get("/catalogs/modelos")
async def list_modelos(service: CatalogService = Depends(get_catalog_service)):
    return await service.get_modelos()

@router.post("/catalogs/modelos")
async def add_modelo(data: ModelCreate, service: CatalogService = Depends(get_catalog_service)):
    return await service.create_modelo(data.model_dump())

@router.delete("/catalogs/{table}/{id}")
async def remove_item(table: str, id: int, service: CatalogService = Depends(get_catalog_service)):
    return await service.delete_item(table, id)

# --- TIPOS DE EQUIPO ---

@router.get("/catalogs/tipos_equipo", response_model=list[CatalogRead])
async def list_tipos(service: CatalogService = Depends(get_catalog_service)):
    return await service.get_tipos_equipo()

@router.post("/catalogs/tipos_equipo", response_model=CatalogRead)
async def add_tipo(data: CatalogCreate, service: CatalogService = Depends(get_catalog_service)):
    return await service.create_tipo_equipo(data.model_dump())

@router.delete("/catalogs/tipos_equipo/{id}")
async def remove_tipo(id: int, service: CatalogService = Depends(get_catalog_service)):
    return await service.delete_tipo_equipo(id)