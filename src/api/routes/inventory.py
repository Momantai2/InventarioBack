from fastapi import APIRouter, HTTPException
from src.schemas.inventory import EquipmentCreate
from src.infrastructure.repositories.equipment_repository_impl import EquipmentRepositoryImpl
from src.domain.entities.equipment import Equipment
from src.api.auth import get_current_user
from src.infrastructure.supabase_client import supabase
from fastapi import Depends
router = APIRouter(tags=["Equipos"])
repo = EquipmentRepositoryImpl()

router = APIRouter()
@router.post("/equipos", dependencies=[Depends(get_current_user)])
async def create_equipment(data: EquipmentCreate):
    # 1. Validar duplicado
    if repo.exists_by_serie(data.serie):
        raise HTTPException(
            status_code=409, 
            detail=f"El número de serie '{data.serie}' ya está registrado en otro equipo."
        )
    
    try:
        new_equipment = Equipment(**data.model_dump())
        result = repo.create(new_equipment)
        return {"message": "Equipo creado con éxito", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/equipos")
async def get_all_equipments():
    return repo.get_all()

# src/api/routes.py

@router.put("/equipos/{equipment_id}")
async def update_equipment(equipment_id: int, data: EquipmentCreate):
    # 1. Validar duplicado (excluyendo el equipo actual)
    if repo.exists_by_serie(data.serie, exclude_id=equipment_id):
        raise HTTPException(
            status_code=409, 
            detail=f"No se puede actualizar: la serie '{data.serie}' ya pertenece a otro equipo."
        )
    
    try:
        update_data = data.model_dump()
        result = repo.update(equipment_id, update_data)
        return {"message": "Equipo actualizado", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/equipos/{equipment_id}")
async def delete_equipment(equipment_id: int):
    try:
        repo.delete(equipment_id)
        return {"message": "Equipo eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para Modelos (incluyendo la marca)
@router.get("/modelos")
async def get_models():
    result = supabase.table("modelos").select("id, nombre, marcas(nombre)").execute()
    return [{"id": m["id"], "nombre": f"{m['marcas']['nombre']} - {m['nombre']}"} for m in result.data]

@router.get("/estados")
async def get_states():
    result = supabase.table("estados").select("id, nombre").execute()
    return result.data

@router.get("/ubicaciones")
async def get_locations():
    # Mejora: formatear el nombre para que el Select se vea bien
    result = supabase.table("ubicaciones_detalladas").select("id, piso_oficina, areas(nombre)").execute()
    return [
        {"id": u["id"], "nombre": f"{u['areas']['nombre']} - {u['piso_oficina']}"} 
        for u in result.data
    ]