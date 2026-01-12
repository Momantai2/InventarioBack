from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from src.infrastructure.supabase_client import supabase  # Ajusta según tu cliente
from src.schemas.person import Person, PersonCreate, PersonUpdate

router = APIRouter()

@router.get("/personas", response_model=List[dict])
async def get_persons(search: Optional[str] = None):
    # Traemos los datos incluyendo el nombre del área (join)
    query = supabase.table("personas").select("*, areas(nombre)")
    
    if search:
        query = query.or_(f"nombre_completo.ilike.%{search}%,dni.ilike.%{search}%")
    
    response = query.order("nombre_completo").execute()
    return response.data

@router.post("/personas", response_model=dict)
async def create_person(person: PersonCreate):
    try:
        # Intentamos insertar en la tabla 'personas'
        response = supabase.table("personas").insert(person.dict()).execute()
        return response.data[0]
    except Exception as e:
        error_str = str(e)
        # 1. Capturar error de DNI Duplicado (Unique Constraint)
        if "duplicate key" in error_str or "already exists" in error_str:
            raise HTTPException(
                status_code=400, 
                detail=f"El DNI {person.dni} ya está registrado."
            )
        
        # 2. Capturar otros errores de base de datos
        raise HTTPException(
            status_code=500, 
            detail="Error interno al procesar el registro."
        )

@router.put("/personas/{person_id}", response_model=dict)
async def update_person(person_id: int, person: PersonUpdate):
    # Solo actualizamos los campos enviados (excluyendo los None)
    update_data = {k: v for k, v in person.dict().items() if v is not None}
    
    response = supabase.table("personas").update(update_data).eq("id", person_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return response.data[0]

@router.delete("personas/{person_id}")
async def delete_person(person_id: int):
    response = supabase.table("personas").delete().eq("id", person_id).execute()
    return {"message": "Persona eliminada correctamente"}

@router.get("/areas", response_model=List[dict])
async def get_areas():
    response = supabase.table("areas").select("*").order("nombre").execute()
    return response.data