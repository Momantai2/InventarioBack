from fastapi import APIRouter, Depends, HTTPException
from src.application.services.MantenimientoService import MantenimientoService
from src.infrastructure.repositories.mantenimiento_repository_impl import MantenimientoRepositoryImpl
from src.infrastructure.repositories.equipment_repository_impl import EquipmentRepositoryImpl
from src.schemas.mantenimiento import (
    MantenimientoCreate, 
    MantenimientoRead, 
    MantenimientoUpdate,
    TipoMantenimientoRead,
    TipoMantenimientoCreate,
    TipoMantenimientoUpdate
)
from typing import List

router = APIRouter(prefix="/mantenimientos", tags=["Gestión Técnica y Mantenimiento"])
router1 = APIRouter(prefix="/tipos_mantenimientos", tags=["Tipos de mantenimiento"])

# Inyección de dependencias
def get_mantenimiento_service():
    mant_repo = MantenimientoRepositoryImpl()
    eq_repo = EquipmentRepositoryImpl()
    return MantenimientoService(mant_repo, eq_repo)

@router.post("/entry", response_model=MantenimientoRead)
async def register_maintenance_entry(
    data: MantenimientoCreate, 
    service: MantenimientoService = Depends(get_mantenimiento_service)
):
    result = await service.register_entry(data.model_dump())
    return result

@router.patch("/exit/{mant_id}/{equipo_id}", response_model=dict)
async def register_maintenance_exit(
    mant_id: int,
    equipo_id: int,
    exit_data: MantenimientoUpdate,
    service: MantenimientoService = Depends(get_mantenimiento_service)
):
    return await service.register_exit(mant_id, equipo_id, exit_data.model_dump(exclude_unset=True))

@router.get("/equipment/{equipo_id}", response_model=List[MantenimientoRead])
async def get_equipment_maintenance_history(
    equipo_id: int,
    service: MantenimientoService = Depends(get_mantenimiento_service)
):
    # CORRECCIÓN: Se añadió el contenido y se eliminó el 'await' del repo sincrónico
    return service.mant_repo.get_by_equipo(equipo_id)

@router.get("/", response_model=List[MantenimientoRead])
async def get_all(service: MantenimientoService = Depends(get_mantenimiento_service)):
    # Si list_mantenimientos en el service NO es async, quita el await aquí también
    return await service.list_mantenimientos()


# --- TIPO MANTENIMIENTO ---

@router1.get("", response_model=List[TipoMantenimientoRead])
async def list_tipos(service: MantenimientoService = Depends(get_mantenimiento_service)):
    return await service.list_all_tipo_mantenimiento()

@router1.get("/{tipo_id}", response_model=TipoMantenimientoRead)
async def get_tipo(tipo_id: int, service: MantenimientoService = Depends(get_mantenimiento_service)):
    return await service.get_one_tipo_mantenimiento(tipo_id)

@router1.post("", response_model=TipoMantenimientoRead)
async def create_tipo(
    data: TipoMantenimientoCreate, 
    service: MantenimientoService = Depends(get_mantenimiento_service)
):
    return await service.create_new_tipo_mantenimiento(data.model_dump())

@router1.patch("/{tipo_id}", response_model=TipoMantenimientoRead)
async def update_tipo(
    tipo_id: int, 
    data: TipoMantenimientoUpdate, 
    service: MantenimientoService = Depends(get_mantenimiento_service)
):
    return await service.update_existing_tipo_mantenimiento(tipo_id, data.model_dump(exclude_unset=True))

@router1.delete("/{tipo_id}")
async def delete_tipo(
    tipo_id: int, 
    service: MantenimientoService = Depends(get_mantenimiento_service)
):
    return await service.remove_tipo_mantenimiento(tipo_id)