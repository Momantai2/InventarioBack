from fastapi import APIRouter, HTTPException
from typing import List
from src.infrastructure.supabase_client import supabase
from src.schemas.organization import (
    GerenciaRead, GerenciaCreate,
    AreaRead, AreaCreate,
    DepartamentoRead, DepartamentoCreate,
    TipoLocalRead, TipoLocalCreate,
    SedeRead, SedeCreate,UbicacionDetalladaCreate,UbicacionDetalladaRead
)

router = APIRouter()

# --- GERENCIAS ---
@router.get("/organizacion/gerencias", response_model=List[GerenciaRead])
def get_gerencias():
    res = supabase.table("gerencias").select("*").order("nombre").execute()
    return res.data

@router.post("/organizacion/gerencias", response_model=GerenciaRead)
def create_gerencia(data: GerenciaCreate):
    res = supabase.table("gerencias").insert({"nombre": data.nombre.upper()}).execute()
    if not res.data: raise HTTPException(status_code=400, detail="Error al crear")
    return res.data[0]

@router.delete("/organizacion/gerencias/{id}")
def delete_gerencia(id: int):
    supabase.table("gerencias").delete().eq("id", id).execute()
    return {"status": "deleted"}

# --- AREAS (Relacionado con Gerencia) ---
@router.get("/organizacion/areas", response_model=List[AreaRead])
def get_areas():
    res = supabase.table("areas").select("*, gerencias(*)").order("nombre").execute()
    return res.data

@router.post("/organizacion/areas", response_model=AreaRead)
def create_area(data: AreaCreate):
    res = supabase.table("areas").insert({
        "nombre": data.nombre.upper(),
        "gerencia_id": data.gerencia_id
    }).execute()
    if not res.data: raise HTTPException(status_code=400, detail="Error al crear área")
    full_res = supabase.table("areas").select("*, gerencias(*)").eq("id", res.data[0]['id']).single().execute()
    return full_res.data

@router.delete("/organizacion/areas/{id}")
def delete_area(id: int):
    supabase.table("areas").delete().eq("id", id).execute()
    return {"status": "deleted"}

# --- DEPARTAMENTOS ---
@router.get("/organizacion/departamentos", response_model=List[DepartamentoRead])
def get_departamentos():
    res = supabase.table("departamentos").select("*").order("nombre").execute()
    return res.data

@router.post("/organizacion/departamentos", response_model=DepartamentoRead)
def create_departamento(data: DepartamentoCreate):
    res = supabase.table("departamentos").insert({"nombre": data.nombre.upper()}).execute()
    return res.data[0]

@router.delete("/organizacion/departamentos/{id}")
def delete_departamento(id: int):
    supabase.table("departamentos").delete().eq("id", id).execute()
    return {"status": "deleted"}

# --- TIPOS DE LOCAL ---
@router.get("/organizacion/tipos_local", response_model=List[TipoLocalRead])
def get_tipos_local():
    res = supabase.table("tipos_local").select("*").order("nombre").execute()
    return res.data

@router.post("/organizacion/tipos_local", response_model=TipoLocalRead)
def create_tipo_local(data: TipoLocalCreate):
    res = supabase.table("tipos_local").insert({"nombre": data.nombre.upper()}).execute()
    return res.data[0]

@router.delete("/organizacion/tipos_local/{id}")
def delete_tipo_local(id: int):
    supabase.table("tipos_local").delete().eq("id", id).execute()
    return {"status": "deleted"}

# --- SEDES AGENCIAS (Relacionado con Departamento y Tipo Local) ---
@router.get("/organizacion/sedes_agencias", response_model=List[SedeRead])
def get_sedes():
    res = supabase.table("sedes_agencias").select("*, departamentos(*), tipos_local(*)").order("nombre").execute()
    return res.data

@router.post("/organizacion/sedes_agencias", response_model=SedeRead)
def create_sede(data: SedeCreate):
    res = supabase.table("sedes_agencias").insert({
        "nombre": data.nombre.upper(),
        "departamento_id": data.departamento_id,
        "tipo_local_id": data.tipo_local_id
    }).execute()
    if not res.data: raise HTTPException(status_code=400, detail="Error al crear sede")
    full_res = supabase.table("sedes_agencias").select("*, departamentos(*), tipos_local(*)").eq("id", res.data[0]['id']).single().execute()
    return full_res.data

@router.delete("/organizacion/sedes_agencias/{id}")
def delete_sede(id: int):
    supabase.table("sedes_agencias").delete().eq("id", id).execute()
    return {"status": "deleted"}

@router.get("/organizacion/ubicaciones_detalladas", response_model=List[UbicacionDetalladaRead])
def get_ubicaciones_detalladas():
    # Esta query trae: Ubicacion -> Area(Gerencia) y Sede(Departamento, TipoLocal)
    res = supabase.table("ubicaciones_detalladas").select("""
        id, 
        area_id, 
        sede_id, 
        piso_oficina,
        areas(*, gerencias(*)),
        sedes_agencias(*, departamentos(*), tipos_local(*))
    """).execute()
    return res.data

@router.post("/organizacion/ubicaciones_detalladas", response_model=UbicacionDetalladaRead)
def create_ubicacion_detallada(data: UbicacionDetalladaCreate):
    res = supabase.table("ubicaciones_detalladas").insert({
        "area_id": data.area_id,
        "sede_id": data.sede_id,
        "piso_oficina": data.piso_oficina.upper()
    }).execute()
    
    if not res.data:
        raise HTTPException(status_code=400, detail="Error al crear la ubicación")
    
    # Recuperamos el objeto completo con relaciones
    nuevo_id = res.data[0]['id']
    full_res = supabase.table("ubicaciones_detalladas").select("""
        id, area_id, sede_id, piso_oficina,
        areas(*, gerencias(*)),
        sedes_agencias(*, departamentos(*), tipos_local(*))
    """).eq("id", nuevo_id).single().execute()
    
    return full_res.data

@router.delete("/organizacion/ubicaciones_detalladas/{id}")
def delete_ubicacion_detallada(id: int):
    supabase.table("ubicaciones_detalladas").delete().eq("id", id).execute()
    return {"status": "deleted"}