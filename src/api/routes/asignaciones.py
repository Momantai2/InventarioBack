from fastapi import APIRouter, Depends, HTTPException, Query
from src.application.services.HistorialAsignacionesService import HistorialAsignacionesService
from src.infrastructure.repositories.historial_asignaciones_repository_impl import HistorialAsignacionesRepositoryImpl
from src.infrastructure.repositories.equipment_repository_impl import EquipmentRepositoryImpl
from src.schemas.historial_asignaciones import HistorialAsignacionesCreate, HistorialAsignacionesRead, BulkAssignRequest

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones e Historial"])

# Inyección de dependencias para el servicio
def get_assignment_service():
    hist_repo = HistorialAsignacionesRepositoryImpl()
    eq_repo = EquipmentRepositoryImpl()
    return HistorialAsignacionesService(hist_repo, eq_repo)

# --- CONSULTAS ---

@router.get("/history", response_model=list[HistorialAsignacionesRead])
async def get_full_history(service: HistorialAsignacionesService = Depends(get_assignment_service)):
    """Obtiene el historial completo de todas las asignaciones realizadas."""
    return await service.list_all_history()

@router.get("/equipment/{equipo_id}", response_model=list[HistorialAsignacionesRead])
async def get_equipment_history(
    equipo_id: int, 
    service: HistorialAsignacionesService = Depends(get_assignment_service)
):
    """Obtiene la línea de tiempo de dueños de un equipo específico."""
    return await service.get_history_by_equipment(equipo_id)

# --- ACCIONES DE MOVIMIENTO ---

@router.post("/assign")
async def assign_equipment(
    data: HistorialAsignacionesCreate, 
    service: HistorialAsignacionesService = Depends(get_assignment_service)
):
    """
    ID 1: Asignación estándar.
    Crea el registro y pone el equipo en estado 'Asignado'.
    """
    return await service.assign_equipment(
        equipo_id=data.equipo_id,
        persona_id=data.persona_id,
        tipo_movimiento_id=1, # Forzamos ID 1 para esta ruta
        obs=data.observaciones
    )

@router.patch("/release/{equipo_id}")
async def release_equipment(
    equipo_id: int, 
    observaciones: str = Query(None),
    service: HistorialAsignacionesService = Depends(get_assignment_service)
):
    """
    ID 2: Devolución.
    Libera el equipo y registra el retorno a almacén en el historial.
    """
    return await service.release_equipment(equipo_id, obs=observaciones)

@router.post("/transfer")
async def transfer_equipment(
    data: HistorialAsignacionesCreate, 
    service: HistorialAsignacionesService = Depends(get_assignment_service)
):
    """
    ID 3: Transferencia directa.
    Pasa el equipo de un usuario a otro sin pasar por almacén.
    """
    # Usamos persona_id del body como el RECEPTOR de la transferencia
    return await service.transfer_equipment(
        equipo_id=data.equipo_id,
        nuevo_persona_id=data.persona_id,
        obs=data.observaciones
    )

@router.delete("/decommission/{equipo_id}")
async def decommission_equipment(
    equipo_id: int,
    observaciones: str = Query(None),
    service: HistorialAsignacionesService = Depends(get_assignment_service)
):
    """
    ID 4: Baja.
    Retira el equipo de circulación por daño, pérdida o robo.
    """
    return await service.decommission_equipment(equipo_id, obs=observaciones)

# --- ACCIONES MASIVAS ---

@router.patch("/bulk-assign")
async def bulk_assign(
    payload: BulkAssignRequest, 
    service: HistorialAsignacionesService = Depends(get_assignment_service)
):
    """Asigna un lote de equipos a una sola persona."""
    return await service.bulk_assign(
        equipo_ids=payload.equipment_ids, 
        persona_id=payload.person_id,
        tipo_movimiento_id=1
    )