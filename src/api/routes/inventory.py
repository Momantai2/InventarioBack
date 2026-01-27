from fastapi import APIRouter, Depends, Query, status
from typing import Optional, List
from src.application.services.EquipmentService import EquipmentService
from src.infrastructure.repositories.equipment_repository_impl import EquipmentRepositoryImpl
from src.schemas.inventory import (
    EquipmentCreate, 
    EquipmentRead, 
    EquipmentUpdate, 
    EquipmentPagedResponse,
    ProveedorRentingRead, 
    ProveedorRentingCreate
)

router = APIRouter(prefix="/equipos-inventario", tags=["Equipos"])

def get_service():
    return EquipmentService(EquipmentRepositoryImpl())

# --- 1. GESTIÓN DE EQUIPOS (CRUD PRINCIPAL) ---

@router.get("/", response_model=EquipmentPagedResponse)
async def list_equipos(
    query: Optional[str] = Query(None, description="Buscar por serie u observaciones"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: EquipmentService = Depends(get_service)
):
    """Listado paginado de equipos con sus relaciones completas."""
    return await service.get_all_equipments(query=query, page=page, page_size=page_size)

@router.post("/", response_model=EquipmentRead, status_code=status.HTTP_201_CREATED)
async def create_equipment(
    data: EquipmentCreate, 
    service: EquipmentService = Depends(get_service)
):
    """Crea un equipo y asigna automáticamente el estado según el usuario."""
    return await service.create_equipment(data.model_dump())

@router.patch("/{id}", response_model=EquipmentRead)
async def update_equipment(
    id: int, 
    updates: EquipmentUpdate, 
    service: EquipmentService = Depends(get_service)
):
    """Actualiza parcialmente un equipo y gestiona la trazabilidad de usuarios."""
    return await service.update_equipment(id, updates.model_dump(exclude_unset=True))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment(id: int, service: EquipmentService = Depends(get_service)):
    """Elimina un equipo del inventario."""
    await service.delete_equipment(id)
    return None

# --- 2. VALIDACIONES Y UTILITARIOS ---

@router.get("/check-serie/{serie}")
async def check_serie_availability(
    serie: str, 
    exclude_id: Optional[int] = Query(None), 
    service: EquipmentService = Depends(get_service)
):
    """Verifica si una serie ya existe para validación en tiempo real en el front."""
    exists = await service.check_serie_availability(serie, exclude_id)
    return {"exists": exists}

# --- 3. RUTAS PARA SELECTS (CATÁLOGOS FORMATEADOS) ---

@router.get("/catalogos/modelos")
async def get_modelos_for_select(service: EquipmentService = Depends(get_service)):
    """Retorna modelos formateados: 'Marca - Modelo'."""
    return await service.get_formatted_models()

@router.get("/catalogos/ubicaciones")
async def get_ubicaciones_for_select(service: EquipmentService = Depends(get_service)):
    """Retorna ubicaciones formateadas: 'Sede - Área (Piso)'."""
    return await service.get_formatted_locations()

@router.get("/catalogos/estados")
async def list_estados(service: EquipmentService = Depends(get_service)):
    """Retorna la lista de estados operativos."""
    return await service.get_all_estados()

# --- 4. PROVEEDORES RENTING ---

@router.get("/proveedores", response_model=List[ProveedorRentingRead])
async def list_proveedores(service: EquipmentService = Depends(get_service)):
    return await service.get_all_proveedores()

@router.post("/proveedores", response_model=ProveedorRentingRead, status_code=status.HTTP_201_CREATED)
async def create_provider(
    data: ProveedorRentingCreate, 
    service: EquipmentService = Depends(get_service)
):
    return await service.create_proveedor(data.model_dump())

@router.get("/proveedores/select")
async def get_proveedores_select_list(service: EquipmentService = Depends(get_service)):
    """Lista simplificada de proveedores para dropdowns."""
    return await service.get_proveedores_for_select()

@router.delete("/proveedores_renting/{id}")
async def delete_provider(id: int, service: EquipmentService = Depends(get_service)):
    return await service.delete_proveedor(id)
