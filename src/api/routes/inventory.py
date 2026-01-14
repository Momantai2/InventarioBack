from fastapi import APIRouter, Depends, Query
from typing import Optional
from src.application.services.EquipmentService import EquipmentService
from src.infrastructure.repositories.equipment_repository_impl import EquipmentRepositoryImpl
from src.schemas.inventory import EquipmentCreate, BulkAssignRequest, ProveedorRentingRead, ProveedorRentingCreate

router = APIRouter(tags=["Equipos"])

def get_service():
    return EquipmentService(EquipmentRepositoryImpl())

# --- 1. RUTAS DE COLECCIÓN / BÚSQUEDA ---
@router.get("/equipos")
async def list_equipos(search: Optional[str] = Query(None), service: EquipmentService = Depends(get_service)):
    return await service.get_all_equipments(search)

@router.get("/check-serie/{serie}")
async def check_serie(
    serie: str, 
    exclude_id: Optional[int] = Query(None), 
    service: EquipmentService = Depends(get_service)
):
    exists = await service.check_serie_availability(serie, exclude_id)
    return {"exists": exists}

# --- 2. RUTAS DE ACCIÓN MASIVA (DEBEN IR ANTES QUE {id}) ---
@router.patch("/equipos/bulk-assign")
async def bulk_assign(
    payload: BulkAssignRequest, 
    service: EquipmentService = Depends(get_service)
):
    return await service.bulk_assign(payload.equipment_ids, payload.person_id)

# --- 3. RUTAS DE CATÁLOGOS ---
@router.get("/modelos")
async def models(service: EquipmentService = Depends(get_service)):
    return await service.get_formatted_models()

@router.get("/ubicaciones")
async def locations(service: EquipmentService = Depends(get_service)):
    return await service.get_formatted_locations()

@router.get("/estados")
async def list_estados(service: EquipmentService = Depends(get_service)):
    return await service.get_all_estados()

# --- 4. RUTAS DINÁMICAS POR ID ---
@router.post("/equipos")
async def create(data: EquipmentCreate, service: EquipmentService = Depends(get_service)):
    return await service.create_equipment(data.model_dump())

@router.patch("/equipos/{id}")
async def update(id: int, updates: dict, service: EquipmentService = Depends(get_service)):
    return await service.update_equipment(id, updates)

@router.delete("/equipos/{id}")
async def delete(id: int, service: EquipmentService = Depends(get_service)):
    return await service.delete_equipment(id)

@router.patch("/equipos/{id}/assign")
async def assign(id: int, data: dict, service: EquipmentService = Depends(get_service)):
    return await service.assign_equipment(id, data.get("personal_usuario_id"))

@router.patch("/equipos/{id}/release")
async def release(id: int, service: EquipmentService = Depends(get_service)):
    return await service.release_equipment(id)

# --- 5. PROVEEDORES RENTING ---
@router.get("/proveedores_renting", response_model=list[ProveedorRentingRead])
async def list_proveedores(service: EquipmentService = Depends(get_service)):
    return await service.get_all_proveedores()

@router.post("/proveedores_renting", response_model=ProveedorRentingRead)
async def create_provider(data: ProveedorRentingCreate, service: EquipmentService = Depends(get_service)):
    return await service.create_proveedor(data.model_dump())

@router.delete("/proveedores_renting/{id}")
async def delete_provider(id: int, service: EquipmentService = Depends(get_service)):
    return await service.delete_proveedor(id)

@router.get("/proveedores_select")
async def get_select_list(service: EquipmentService = Depends(get_service)):
    return await service.get_proveedores_for_select()