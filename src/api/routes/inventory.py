from fastapi import APIRouter, HTTPException
from src.schemas.inventory import EquipmentCreate
from src.infrastructure.repositories.equipment_repository_impl import EquipmentRepositoryImpl
from src.domain.entities.equipment import Equipment
from src.api.auth import get_current_user
from src.infrastructure.supabase_client import supabase
from fastapi import Depends
from datetime import datetime
from typing import Optional

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
async def get_all_equipments(search: Optional[str] = None):
    try:
        # La clave es: personas(...) -> areas(...) -> jefes:personas!area_id(...)
        # Esto trae a los jefes dentro de la estructura del usuario asignado
        query = supabase.table("equipos").select("""
            *,
            modelos(nombre, marcas(nombre)),
            estados(nombre),
            ubicaciones_detalladas(piso_oficina, areas(nombre)),
            proveedores_renting(nombre),
            personas:personas!equipos_personal_usuario_id_fkey(
                nombre_completo, 
                dni, 
                areas(
                    id,
                    nombre, 
                    jefes:personas!area_id(nombre_completo, jefe_area)
                )
            ),
            anterior:personas!equipos_personal_anterior_id_fkey(nombre_completo)
        """)
        
        if search:
            query = query.ilike("serie", f"%{search}%")
            
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}") # Esto lo verás en la consola de tu terminal
        raise HTTPException(status_code=500, detail=str(e))
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
    
@router.patch("/equipos/{eq_id}/assign")
async def assign_equipment(eq_id: int, data: dict):
    nuevo_usuario_id = data.get("personal_usuario_id")
    ahora = datetime.now().isoformat()
    
    # Define aquí los IDs de tus estados según tu base de datos
    ESTADO_ASIGNADO = 2 
    ESTADO_BAJA = 4

    try:
        # 1. Obtener datos actuales (incluyendo el estado)
        current_res = supabase.table("equipos")\
            .select("personal_usuario_id, estado_id")\
            .eq("id", eq_id)\
            .single().execute()
        
        if not current_res.data:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        equipo_actual = current_res.data
        
        # 2. VALIDACIÓN: Si el equipo está de BAJA, no se puede asignar
        if equipo_actual.get("estado_id") == ESTADO_BAJA:
            raise HTTPException(
                status_code=400, 
                detail="No se puede asignar este equipo porque está marcado como 'INOPERATIVA'."
            )

        # 3. Preparar datos de actualización
        usuario_previo_id = equipo_actual.get("personal_usuario_id")
        
        update_data = {
            "personal_usuario_id": nuevo_usuario_id,
            "fecha_asignacion": ahora,
            "estado_id": ESTADO_ASIGNADO  # Actualización automática de estado
        }

        # 4. Lógica de Historial (Rotación)
        if usuario_previo_id and usuario_previo_id != nuevo_usuario_id:
            update_data["personal_anterior_id"] = usuario_previo_id
            update_data["fecha_devolucion"] = ahora

        # 5. Ejecutar cambios
        response = supabase.table("equipos").update(update_data).eq("id", eq_id).execute()
        
        return {
            "message": "Equipo asignado exitosamente y estado actualizado a 'Asignado'",
            "data": response.data[0]
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en el proceso: {str(e)}")
    
@router.patch("/equipos/{eq_id}/release")
async def release_equipment(eq_id: int):
    ahora = datetime.now().isoformat()
    ESTADO_DISPONIBLE = 1 # ID de 'Operativo/Disponible' en tu BD

    try:
        # 1. Obtener quién tiene el equipo actualmente
        current_res = supabase.table("equipos")\
            .select("personal_usuario_id")\
            .eq("id", eq_id)\
            .single().execute()
        
        if not current_res.data:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        usuario_actual_id = current_res.data.get("personal_usuario_id")

        if not usuario_actual_id:
            return {"message": "El equipo ya se encuentra liberado"}

        # 2. Preparar la liberación
        release_data = {
            "personal_usuario_id": None,      # Quitamos al dueño actual
            "personal_anterior_id": usuario_actual_id, # Lo movemos al historial
            "fecha_devolucion": ahora,        # Registramos cuándo lo entregó
            "estado_id": ESTADO_DISPONIBLE,   # Lo volvemos a poner disponible
            "fecha_asignacion": None          # Limpiamos la fecha de asignación actual
        }

        # 3. Ejecutar actualización
        response = supabase.table("equipos").update(release_data).eq("id", eq_id).execute()
        
        return {"message": "Equipo liberado correctamente", "data": response.data[0]}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al liberar: {str(e)}")
    
@router.patch("/equipos/bulk-assign")
async def bulk_assign_equipment(payload: dict):
    """
    Payload esperado:
    {
        "equipment_ids": [101, 102, 105],
        "person_id": 5
    }
    """
    ids = payload.get("equipment_ids")
    person_id = payload.get("person_id")
    
    if not ids or not person_id:
        raise HTTPException(status_code=400, detail="Faltan IDs de equipos o de la persona")

    try:
        # Fecha actual para el registro de asignación
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Actualizamos todos los equipos cuyo ID esté en la lista
        response = supabase.table("equipos").update({
            "personal_usuario_id": person_id,
            "fecha_asignacion": fecha_actual,
            "estado_id": 2, # Suponiendo que 2 es 'Asignado'
        }).in_("id", ids).execute()

        return {"status": "success", "message": f"{len(ids)} equipos asignados correctamente"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))