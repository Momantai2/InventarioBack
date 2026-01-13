from fastapi import APIRouter, HTTPException
from typing import List
from src.infrastructure.supabase_client import supabase  
from src.schemas.catalog import CatalogRead, CatalogCreate,  ModelRead, ModelCreate
router = APIRouter()

# --- MARCAS ---
@router.get("/catalogs/marcas", response_model=List[CatalogRead])
def get_marcas():
    res = supabase.table("marcas").select("*").order("nombre").execute()
    return res.data

@router.post("/catalogs/marcas", response_model=CatalogRead)
def create_marca(data: CatalogCreate):
    res = supabase.table("marcas").insert({"nombre": data.nombre.upper()}).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Error al crear marca")
    return res.data[0]

@router.delete("/catalogs/marcas/{id}")
def delete_marca(id: int):
    supabase.table("marcas").delete().eq("id", id).execute()
    return {"status": "deleted"}

# --- TIPOS DE EQUIPO ---
@router.get("/catalogs/tipos_equipo", response_model=List[CatalogRead])
def get_tipos():
    res = supabase.table("tipos_equipo").select("*").order("nombre").execute()
    return res.data

@router.post("/catalogs/tipos_equipo", response_model=CatalogRead)
def create_tipo(data: CatalogCreate):
    res = supabase.table("tipos_equipo").insert({"nombre": data.nombre.upper()}).execute()
    return res.data[0]

@router.delete("/catalogs/tipos_equipo/{id}")
def delete_tipo(id: int):
    supabase.table("tipos_equipo").delete().eq("id", id).execute()
    return {"status": "deleted"}

# --- MODELOS ---

@router.get("/catalogs/modelos", response_model=List[ModelRead])
def get_modelos():
    # Intentaremos una selección explícita para forzar el JOIN
    res = supabase.table("modelos")\
        .select("""
            id, 
            nombre, 
            marca_id, 
            tipo_equipo_id, 
            marcas!inner(id, nombre), 
            tipos_equipo!inner(id, nombre)
        """)\
        .order("nombre")\
        .execute()
    
    return res.data

@router.post("/catalogs/modelos", response_model=ModelRead)
def create_modelo(data: ModelCreate):
    # Insertamos los datos básicos
    res = supabase.table("modelos").insert({
        "nombre": data.nombre.upper(),
        "marca_id": data.marca_id,
        "tipo_equipo_id": data.tipo_equipo_id
    }).execute()
    
    if not res.data:
        raise HTTPException(status_code=400, detail="Error al crear el modelo")
    
    # Para devolver el objeto completo con sus relaciones, consultamos el ID recién creado
    nuevo_id = res.data[0]['id']
    modelo_completo = supabase.table("modelos").select("*, marcas(*), tipos_equipo(*)").eq("id", nuevo_id).single().execute()
    
    return modelo_completo.data

@router.delete("/catalogs/modelos/{id}")
def delete_modelo(id: int):
    # Nota: Esto fallará si hay equipos usando este modelo (Restricción de Integridad)
    try:
        supabase.table("modelos").delete().eq("id", id).execute()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="No se puede eliminar: el modelo está en uso por equipos.")