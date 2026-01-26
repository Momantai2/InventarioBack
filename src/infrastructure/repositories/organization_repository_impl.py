from src.infrastructure.supabase_client import supabase
from typing import Optional
class OrganizationRepositoryImpl:
    def __init__(self):
        pass


# AHORA
    def get_gerencias(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        # Iniciamos la consulta base
        db_query = supabase.table("gerencias").select("*", count="exact").eq("activo", True)
        
        # Si el usuario envió una búsqueda, aplicamos el filtro
        if query:
            db_query = db_query.ilike("nombre", f"%{query}%")
            
        res = db_query.order("nombre").range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_gerencia_by_id(self, gerencia_id: int):
        return supabase.table("gerencias").select("*").eq("id", gerencia_id).single().execute().data

    def get_gerencia_by_name(self, nombre: str):
        res = supabase.table("gerencias").select("*").ilike("nombre", nombre.strip()).execute()
        return res.data[0] if res.data else None

    def create_gerencia(self, data: dict):
        res = supabase.table("gerencias").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_gerencia(self, gerencia_id: int, data: dict):
        return supabase.table("gerencias").update(data).eq("id", gerencia_id).execute().data[0]

    def has_active_areas(self, gerencia_id: int) -> bool:
        res = supabase.table("areas").select("id").eq("gerencia_id", gerencia_id).eq("activo", True).execute()
        return len(res.data) > 0
    
    
    def get_areas(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        db_query = supabase.table("areas").select("* , gerencias(id,nombre)", count="exact").eq("activo", True)
        
        if query:
            db_query = db_query.ilike("nombre", f"%{query}%")
            
        res = db_query.order("nombre").range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_area_by_id(self, area_id: int):
        return supabase.table("areas").select("*").eq("id", area_id).single().execute().data

    def get_area_by_name(self, nombre: str):
        res = supabase.table("areas").select("*").ilike("nombre", nombre.strip()).execute()
        return res.data[0] if res.data else None

    def create_area(self, data: dict):
        res = supabase.table("areas").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_area(self, area_id: int, data: dict):
        return supabase.table("areas").update(data).eq("id", area_id).execute().data[0]

    def has_active_area(self, area_id: int) -> bool:
        res = supabase.table("ubicaciones_detalladas").select("id").eq("area_id", area_id).eq("activo", True).execute()
        return len(res.data) > 0
    
    
    def get_departamentos(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        db_query = supabase.table("departamentos").select("*", count="exact").eq("activo", True)
        
        if query:
            db_query = db_query.ilike("nombre", f"%{query}%")
            
        res = db_query.order("nombre").range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_departamento_by_id(self, departamento_id: int):
        return supabase.table("departamentos").select("*").eq("id", departamento_id).single().execute().data

    def get_departamento_by_name(self, nombre: str):
        res = supabase.table("departamentos").select("*").ilike("nombre", nombre.strip()).execute()
        return res.data[0] if res.data else None

    def create_departamento(self, data: dict):
        res = supabase.table("departamentos").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_departamento(self, departamento_id: int, data: dict):
        return supabase.table("departamentos").update(data).eq("id", departamento_id).execute().data[0]

    def has_active_departamento(self, departamento_id: int) -> bool:
        res = supabase.table("sedes_agencias").select("id").eq("departamento_id", departamento_id).eq("activo", True).execute()
        return len(res.data) > 0
    
    
    def get_tipos_local(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        db_query = supabase.table("tipos_local").select("*", count="exact").eq("activo", True)
        
        if query:
            db_query = db_query.ilike("nombre", f"%{query}%")
            
        res = db_query.order("nombre").range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_tipo_local_by_id(self, tipos_local_id: int):
        return supabase.table("tipos_local").select("*").eq("id", tipos_local_id).single().execute().data

    def get_tipo_local_by_name(self, nombre: str):
        res = supabase.table("tipos_local").select("*").ilike("nombre", nombre.strip()).execute()
        return res.data[0] if res.data else None

    def create_tipo_local(self, data: dict):
        res = supabase.table("tipos_local").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_tipo_local(self, tipos_local_id: int, data: dict):
        return supabase.table("tipos_local").update(data).eq("id", tipos_local_id).execute().data[0]

    def has_active_tipo_local(self, tipos_local_id: int) -> bool:
        res = supabase.table("sedes_agencias").select("id").eq("tipo_local_id", tipos_local_id).eq("activo", True).execute()
        return len(res.data) > 0
    
    
    def get_sedes_agencias(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        db_query = supabase.table("sedes_agencias").select("* , tipos_local(id,nombre), departamentos(id,nombre)", count="exact").eq("activo", True)

        if query:
            db_query = db_query.ilike("nombre", f"%{query}%")
            
        res = db_query.order("nombre").range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_sede_agencia_by_id(self, sede_agencia_id: int):
        return supabase.table("sedes_agencias").select("*").eq("id", sede_agencia_id).single().execute().data

    def get_sede_agencia_by_name(self, nombre: str):
        res = supabase.table("sedes_agencias").select("*").ilike("nombre", nombre.strip()).execute()
        return res.data[0] if res.data else None

    def create_sede_agencia(self, data: dict):
        res = supabase.table("sedes_agencias").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_sede_agencia(self, sede_agencia_id: int, data: dict):
        return supabase.table("sedes_agencias").update(data).eq("id", sede_agencia_id).execute().data[0]

    def has_active_sede_agencia(self, sede_agencia_id: int) -> bool:
        res = supabase.table("sedes_agencias").select("id").eq("sede_id", sede_agencia_id).eq("activo", True).execute()
        return len(res.data) > 0
    
    
    def get_ubicaciones_detalladas(self, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1

        res = ( supabase.table("ubicaciones_detalladas").select("""*, areas(id, nombre, gerencias(id, nombre)), sedes_agencias(id,nombre,departamentos(id, nombre),tipos_local(id, nombre))""",count="exact")
        .eq("activo", True)
        .order("created_at")
        .range(start, end)
        .execute()
    )

        return {
        "items": res.data,
        "total": res.count
    }
    def get_ubicacion_detallada_by_id(self, ubicacion_detallada_id: int):
        return supabase.table("ubicaciones_detalladas").select("*").eq("id", ubicacion_detallada_id).single().execute().data
    
    def create_ubicacion_detallada(self, data: dict):
        res = supabase.table("ubicaciones_detalladas").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_ubicacion_detallada(self, ubicacion_detallada_id: int, data: dict):
        return supabase.table("ubicaciones_detalladas").update(data).eq("id", ubicacion_detallada_id).execute().data[0]

    def has_active_ubicacion_detallada(self, ubicacion_detallada_id: int) -> bool:
        res = supabase.table("equipos").select("id").eq("ubicacion_id", ubicacion_detallada_id).eq("activo", True).execute()
        return len(res.data) > 0
    

    