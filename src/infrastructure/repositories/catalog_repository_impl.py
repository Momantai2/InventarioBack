from src.infrastructure.supabase_client import supabase
from typing import Optional

class CatalogRepositoryImpl:
    def __init__(self):
        pass

    def get_marcas(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        db_query = supabase.table("marcas").select("*", count="exact").eq("activo", True)
        
        if query:
            db_query = db_query.ilike("nombre", f"%{query}%")
            
        res = db_query.order("nombre").range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_marca_by_id(self, marca_id: int):
        return supabase.table("marcas").select("*").eq("id", marca_id).single().execute().data

    def get_marca_by_name(self, nombre: str):
        res = supabase.table("marcas").select("*").ilike("nombre", nombre.strip()).execute()
        return res.data[0] if res.data else None

    def create_marca(self, data: dict):
        res = supabase.table("marcas").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_marca(self, marca_id: int, data: dict):
        return supabase.table("marcas").update(data).eq("id", marca_id).execute().data[0]

    def has_active_marcas(self, marca_id: int) -> bool:
        res = supabase.table("modelos").select("id").eq("marca_id", marca_id).eq("activo", True).execute()
        return len(res.data) > 0
    
    
    def get_tipos_equipo(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        db_query = supabase.table("tipos_equipo").select("*", count="exact").eq("activo", True)
        
        if query:
            db_query = db_query.ilike("nombre", f"%{query}%")
            
        res = db_query.order("nombre").range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_tipos_equipo_by_id(self, tipos_equipo_id: int):
        return supabase.table("tipos_equipo").select("*").eq("id", tipos_equipo_id).single().execute().data

    def get_tipos_equipo_by_name(self, nombre: str):
        res = supabase.table("tipos_equipo").select("*").ilike("nombre", nombre.strip()).execute()
        return res.data[0] if res.data else None

    def create_tipos_equipo(self, data: dict):
        res = supabase.table("tipos_equipo").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_tipos_equipo(self, tipos_equipo_id: int, data: dict):
        return supabase.table("tipos_equipo").update(data).eq("id", tipos_equipo_id).execute().data[0]

    def has_active_tipos_equipo(self, tipos_equipo_id: int) -> bool:
        res = supabase.table("modelos").select("id").eq("tipo_equipo_id", tipos_equipo_id).eq("activo", True).execute()
        return len(res.data) > 0


    def get_estados(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        db_query = supabase.table("estados").select("*", count="exact").eq("activo", True)
        
        if query:
            db_query = db_query.ilike("nombre", f"%{query}%")
            
        res = db_query.order("nombre").range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_estados_by_id(self, estado_id: int):
        return supabase.table("estados").select("*").eq("id", estado_id).single().execute().data

    def get_estados_by_name(self, nombre: str):
        res = supabase.table("estados").select("*").ilike("nombre", nombre.strip()).execute()
        return res.data[0] if res.data else None

    def create_estados(self, data: dict):
        res = supabase.table("estados").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_estados(self, estado_id: int, data: dict):
        return supabase.table("estados").update(data).eq("id", estado_id).execute().data[0]

    def has_active_estados(self, estado_id: int) -> bool:
        res = supabase.table("equipos").select("id").eq("estado_id", estado_id).eq("activo", True).execute()
        return len(res.data) > 0


    def get_modelos(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        db_query = supabase.table("modelos").select("* , marcas(id,nombre), tipos_equipo(id,nombre)", count="exact").eq("activo", True)
        
        if query:
            db_query = db_query.ilike("nombre", f"%{query}%")
            
        res = db_query.order("nombre").range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_modelo_by_id(self, modelo_id: int):
        return supabase.table("modelos").select("*").eq("id", modelo_id).single().execute().data

    def get_modelo_by_name(self, nombre: str):
        res = supabase.table("modelos").select("*").ilike("nombre", nombre.strip()).execute()
        return res.data[0] if res.data else None

    def create_modelo(self, data: dict):
        res = supabase.table("modelos").insert(data).execute()
        if not res.data:
            return None 
        return res.data[0]

    def update_modelo(self, modelo_id: int, data: dict):
        return supabase.table("modelos").update(data).eq("id", modelo_id).execute().data[0]

    def has_active_modelo(self, modelo_id: int) -> bool:
        res = supabase.table("equipos").select("id").eq("modelo_id", modelo_id).eq("activo", True).execute()
        return len(res.data) > 0
    