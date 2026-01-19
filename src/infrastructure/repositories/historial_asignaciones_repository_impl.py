from src.infrastructure.supabase_client import supabase
from datetime import datetime
class HistorialAsignacionesRepositoryImpl:
    def get_all_historial(self):
        return supabase.table("historial_asignaciones")\
            .select("*, equipos(serie), personas(nombre_completo), tipos_movimiento_historial(nombre)")\
            .order("fecha_inicio", desc=True)\
            .execute().data

    def get_active_by_equipo(self, equipo_id: int):
        """Busca si el equipo ya tiene una asignación abierta."""
        result = supabase.table("historial_asignaciones")\
            .select("*")\
            .eq("equipo_id", equipo_id)\
            .is_("fecha_fin", "null")\
            .execute()
        return result.data[0] if result.data else None

    def create_historial(self, data: dict):
        result = supabase.table("historial_asignaciones").insert(data).execute()
        return result.data[0]

    def close_assignment(self, historial_id: int, fecha_fin: datetime):
        """Pone fecha de fin a una asignación actual."""
        return supabase.table("historial_asignaciones")\
            .update({"fecha_fin": fecha_fin.isoformat()})\
            .eq("id", historial_id)\
            .execute()
            
    def get_by_equipo(self, equipo_id: int):
        return supabase.table("historial_asignaciones")\
            .select("*, equipos(serie), personas(nombre_completo), tipos_movimiento_historial(nombre)")\
            .eq("equipo_id", equipo_id)\
            .order("fecha_inicio", desc=True)\
            .execute().data

    def get_active_assignment_details(self, equipo_id: int):
        result = supabase.table("historial_asignaciones")\
         .select("id, persona_id, fecha_inicio")\
         .eq("equipo_id", equipo_id)\
         .is_("fecha_fin", "null")\
         .execute()
        return result.data[0] if result.data else None
    
    