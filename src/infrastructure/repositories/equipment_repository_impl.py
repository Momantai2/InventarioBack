from typing import List, Dict, Any
from src.infrastructure.supabase_client import supabase
from datetime import datetime
class EquipmentRepositoryImpl:
    def __init__(self):
        self.table = "equipos"

    def get_by_id(self, equipment_id: int) -> Dict[str, Any]:
        """Obtiene datos básicos de un equipo para validaciones de negocio."""
        result = supabase.table(self.table).select("id, serie, personal_usuario_id, estado_id")\
            .eq("id", equipment_id).single().execute()
        return result.data

    def get_all(self, search: str = None) -> List[Dict[str, Any]]:
        """Consulta pesada con JOINs para la tabla principal."""
        query = supabase.table(self.table).select("""
            *,
            modelos(nombre, marcas(nombre), tipos_equipo(nombre) ),
            estados(nombre),
            ubicaciones_detalladas(piso_oficina, areas(nombre),sedes_agencias(*))),
            proveedores_renting(nombre),
            personas:personas!equipos_personal_usuario_id_fkey(
                nombre_completo, dni, 
                areas(id, nombre, jefes:personas!area_id(nombre_completo, jefe_area))
            ),
            anterior:personas!equipos_personal_anterior_id_fkey(nombre_completo)
        """)
        
        if search:
            query = query.ilike("serie", f"%{search}%")
            
        return query.execute().data

    def create_data(self, data: dict) -> Dict[str, Any]:
        result = supabase.table(self.table).insert(data).execute()
        return result.data[0]

    def update(self, equipment_id: int, data: dict) -> Dict[str, Any]:
        result = supabase.table(self.table).update(data).eq("id", equipment_id).execute()
        return result.data[0]

    def delete(self, equipment_id: int):
        return supabase.table(self.table).delete().eq("id", equipment_id).execute()

    def bulk_update_assign(self, ids: list, person_id: int):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        return supabase.table(self.table).update({
            "personal_usuario_id": person_id,
            "fecha_asignacion": fecha_actual,
            "estado_id": 2,
        }).in_("id", ids).execute()

    # --- Consultas para Catálogos (Raw Data) ---
    def get_models_raw(self):
        return supabase.table("modelos").select("id, nombre, marcas(nombre)").execute().data

    def get_locations_raw(self):
        return supabase.table("ubicaciones_detalladas").select("""
            id, piso_oficina, areas(nombre), sedes_agencias(nombre)
        """).execute().data 
    
    # Agregar estos métodos a EquipmentRepositoryImpl en src/infrastructure/repositories/equipment_repository_impl.py

    def get_proveedores_renting(self):
        return supabase.table("proveedores_renting").select("*").order("nombre").execute().data

    def create_proveedor_renting(self, data: dict):
        result = supabase.table("proveedores_renting").insert(data).execute()
        return result.data[0]

    def get_proveedores_select(self):
        return supabase.table("proveedores_renting").select("id, nombre").execute().data
    
    def get_estados(self):
        """Consulta la tabla de estados ordenada por ID."""
        return supabase.table("estados").select("*").order("id").execute().data

    def get_estado_by_id(self, estado_id: int):
        return supabase.table("estados").select("*").eq("id", estado_id).single().execute().data

    def exists_by_serie(self, serie: str, exclude_id: int = None) -> bool:
        """Verifica la existencia de una serie en la base de datos."""
        # 1. Preparamos la consulta base
        query = supabase.table("equipos").select("id").ilike("serie", serie)
    
        # 2. Aplicamos el filtro de exclusión si es necesario (para edición)
        if exclude_id:
            query = query.neq("id", exclude_id)
        
        # 3. EJECUTAMOS (Fuera del if para que siempre se asigne la variable)
        result = query.execute()
    
        # 4. Retornamos si hay datos
        return len(result.data) > 0