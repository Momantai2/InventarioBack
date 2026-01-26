from typing import Optional, Dict, Any
from src.infrastructure.supabase_client import supabase

class PersonRepositoryImpl:
    def __init__(self):
        self.table = "personas"

    def get_all_paginated(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        """
        Obtiene personas paginadas con sus áreas y la información de jefes de área.
        """
        start = (page - 1) * page_size
        end = start + page_size - 1

        # Consulta base con el JOIN complejo que solicitaste
        # El count="exact" es vital para la paginación
        db_query = supabase.table(self.table).select("""
            *,
            areas (
                id,
                nombre,
                jefes:personas!area_id (
                    nombre_completo,
                    jefe_area
                )
            )
        """, count="exact")

        # Filtro de búsqueda por DNI o Nombre
        if query:
            db_query = db_query.or_(f"nombre_completo.ilike.%{query}%,dni.ilike.%{query}%")

        # Aplicamos orden y rango de paginación
        res = db_query.order("nombre_completo").range(start, end).execute()

        return {
            "items": res.data,
            "total": res.count
        }

    def get_by_id(self, person_id: int) -> Optional[Dict[str, Any]]:
        # Usamos .single() porque buscamos por ID único
        res = supabase.table(self.table).select("*").eq("id", person_id).execute()
        return res.data[0] if res.data else None

    def get_by_dni(self, dni: str) -> Optional[Dict[str, Any]]:
        res = supabase.table(self.table).select("*").eq("dni", dni.strip()).execute()
        return res.data[0] if res.data else None

    def exists_by_dni(self, dni: str, exclude_id: Optional[int] = None) -> bool:
        db_query = supabase.table(self.table).select("id").eq("dni", dni.strip())
        if exclude_id:
            db_query = db_query.neq("id", exclude_id)
        
        res = db_query.execute()
        return len(res.data) > 0

    def create(self, data: dict) -> Dict[str, Any]:
        # Recordatorio: No usamos .single() en inserts para evitar errores de tipo
        res = supabase.table(self.table).insert(data).execute()
        return res.data[0]

    def update(self, person_id: int, data: dict) -> Dict[str, Any]:
        res = supabase.table(self.table).update(data).eq("id", person_id).execute()
        return res.data[0]

    def has_active_personas(self, person_id: int) -> bool:
        """Verificación antes de eliminar (Integridad Referencial)"""
        # Suponiendo que la tabla de equipos tiene un campo responsable_id
        res = supabase.table("equipos").select("id").eq("personal_usuario_id", person_id).eq("activo", True).execute()
        return len(res.data) > 0

    def delete(self, person_id: int):
        return supabase.table(self.table).delete().eq("id", person_id).execute()
    
    def get_jefe_by_area(self, area_id: int):
        res = supabase.table(self.table).select("id, nombre_completo, dni") \
            .eq("area_id", area_id) \
            .eq("jefe_area", True) \
         .eq("activo", True) \
         .execute()
    
    # Retornamos el primero encontrado o None
        return res.data[0] if res.data else None