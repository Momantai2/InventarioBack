from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.schemas.insumos import InsumoRead, InsumoCreate, MovimientoInsumoCreate, Insumo_Movimiento_Read
from src.application.services.InsumoService import InsumoService
from src.infrastructure.repositories.insumos_repository_impl import InsumoRepositoryImpl

router = APIRouter(prefix="/insumos", tags=["Insumos"])
router1 = APIRouter(prefix="/movimientos_insumos", tags=["Movimientos Insumos"])

def get_insumo_service():
    repo = InsumoRepositoryImpl()
    return InsumoService(repo)

# ==========================================
# TABLA INSUMOS (router)
# ==========================================

@router.get("/", response_model=List[InsumoRead])
async def get_all_insumos(service: InsumoService = Depends(get_insumo_service)):
    return await service.list_insumos()

@router.get("/alertas", response_model=List[InsumoRead]) # CORREGIDO: response_model correcto
async def get_stock_alerts(service: InsumoService = Depends(get_insumo_service)):
    return await service.list_alertas_stock()

@router.post("/", response_model=InsumoRead)
async def create_insumo(data: InsumoCreate, service: InsumoService = Depends(get_insumo_service)):
    return await service.add_insumo(data.model_dump())

@router.put("/{id}", response_model=InsumoRead)
async def update_insumo(id: int, data: InsumoCreate, service: InsumoService = Depends(get_insumo_service)):
    return await service.modify_insumo(id, data.model_dump())

@router.delete("/{id}")
async def delete_insumo(id: int, service: InsumoService = Depends(get_insumo_service)):
    await service.remove_insumo(id)
    return {"message": "Insumo eliminado correctamente"}


# ==========================================
# TABLA MOVIMIENTOS INSUMOS (router1)
# ==========================================

@router1.get("/", response_model=List[Insumo_Movimiento_Read])
async def get_all_movimientos(service: InsumoService = Depends(get_insumo_service)):
    # CORREGIDO: Antes llamaba a list_insumos por error
    return await service.list_movimientos_insumos()

@router1.post("/")
async def registrar_transaccion(
    data: MovimientoInsumoCreate, 
    service: InsumoService = Depends(get_insumo_service)
):
    try:
        return await service.registrar_movimiento(data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router1.get("/persona/{persona_id}", response_model=List[Insumo_Movimiento_Read])
async def get_movimientos_by_persona(persona_id: int, service: InsumoService = Depends(get_insumo_service)):
    return await service.repo.get_movimientos_by_persona(persona_id)

# Nota: Normalmente los movimientos (Kardex) no se editan ni eliminan para mantener integridad,
# pero si lo necesitas, asegúrate de que los nombres de función sean únicos.