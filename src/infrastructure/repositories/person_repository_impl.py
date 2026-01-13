from typing import List, Dict, Any
from src.infrastructure.supabase_client import supabase

class PersonRepositoryImpl:
    def __init__(self):
        self.table = "personas"

    def get_all(self, search: str = None) -> List[Dict[str, Any]]:
        query = supabase.table(self.table).select("*, areas(nombre)")
        if search:
            query = query.or_(f"nombre_completo.ilike.%{search}%,dni.ilike.%{search}%")
        return query.order("nombre_completo").execute().data

    def get_by_id(self, person_id: int) -> Dict[str, Any]:
        result = supabase.table(self.table).select("*").eq("id", person_id).single().execute()
        return result.data

    def exists_by_dni(self, dni: str, exclude_id: int = None) -> bool:
        query = supabase.table(self.table).select("id").eq("dni", dni)
        if exclude_id:
            query = query.neq("id", exclude_id)
        result = query.execute()
        return len(result.data) > 0

    def create(self, data: dict) -> Dict[str, Any]:
        result = supabase.table(self.table).insert(data).execute()
        return result.data[0]

    def update(self, person_id: int, data: dict) -> Dict[str, Any]:
        result = supabase.table(self.table).update(data).eq("id", person_id).execute()
        return result.data[0]

    def delete(self, person_id: int):
        return supabase.table(self.table).delete().eq("id", person_id).execute()

    def get_areas(self):
        return supabase.table("areas").select("*").order("nombre").execute().data