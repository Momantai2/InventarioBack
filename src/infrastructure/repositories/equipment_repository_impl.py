from typing import List, Dict, Any, Optional
from src.infrastructure.supabase_client import supabase
from datetime import datetime

class EquipmentRepositoryImpl:
    def __init__(self):
        self.table = "equipos"

    def get_all_paginated(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        """
        Obtiene equipos con paginación y Joins detallados.
        """
        start = (page - 1) * page_size
        end = start + page_size - 1

        # Query base con toda la jerarquía de relaciones
        db_query = supabase.table(self.table).select("""
            *,
            modelos(id, nombre, marcas(nombre), tipos_equipo(nombre)),
            estados(id, nombre),
            ubicaciones_detalladas(id, piso_oficina, areas(nombre), sedes_agencias(nombre)),
            proveedores_renting(id, nombre),
            personas:personas!personal_usuario_id(
                id, nombre_completo, dni, 
                areas(id, nombre, jefes:personas!area_id(nombre_completo, jefe_area))
            ),
            anterior:personas!personal_anterior_id(id, nombre_completo, dni)
        """, count="exact")

        if query:
            # Buscamos por serie, nombre del modelo o nombre del usuario asignado
            # Nota: Supabase or() requiere que las columnas existan en la tabla base 
            # o usar filtros ilike específicos.
            db_query = db_query.or_(f"serie.ilike.%{query}%,observaciones.ilike.%{query}%")

        # Ordenamos por fecha de creación para ver lo más reciente arriba
        res = db_query.order("created_at", desc=True).range(start, end).execute()
        
        return {
            "items": res.data,
            "total": res.count
        }

    def get_by_id(self, equipment_id: int) -> Optional[Dict[str, Any]]:
     # Especificamos explícitamente la relación del usuario actual con !
     result = supabase.table(self.table).select("""
        *, 
        modelos(*), 
        personas:personas!personal_usuario_id(*)
    """).eq("id", equipment_id).execute()
    
     return result.data[0] if result.data else None

    def exists_by_serie(self, serie: str, exclude_id: Optional[int] = None) -> bool:
        db_query = supabase.table(self.table).select("id").ilike("serie", serie.strip())
        if exclude_id:
            db_query = db_query.neq("id", exclude_id)
        result = db_query.execute()
        return len(result.data) > 0

    def create_data(self, data: dict) -> Dict[str, Any]:
        result = supabase.table(self.table).insert(data).execute()
        return result.data[0]

    def update(self, equipment_id: int, data: dict) -> Dict[str, Any]:
        result = supabase.table(self.table).update(data).eq("id", equipment_id).execute()
        return result.data[0]

    def delete(self, equipment_id: int):
        return supabase.table(self.table).delete().eq("id", equipment_id).execute()

    # --- Métodos de apoyo para Selects en el Frontend ---
    
    def get_modelos_for_select(self):
        return supabase.table("modelos").select("id, nombre, marcas(nombre)").eq("activo", True).execute().data

    def get_ubicaciones_for_select(self):
        return supabase.table("ubicaciones_detalladas").select("""
            id, piso_oficina, areas(nombre), sedes_agencias(nombre)
        """).eq("activo", True).execute().data
    
    # Agrega o corrige esto en EquipmentRepositoryImpl
    def get_estados(self):
        """Consulta la tabla de estados ordenada por ID."""
        return supabase.table("estados").select("*").order("id").execute().data

    # Agregar estos métodos a EquipmentRepositoryImpl en src/infrastructure/repositories/equipment_repository_impl.py

    def get_proveedores_renting(self):
        return supabase.table("proveedores_renting").select("*").order("nombre").execute().data

    def create_proveedor_renting(self, data: dict):
        result = supabase.table("proveedores_renting").insert(data).execute()
        return result.data[0]

    def get_proveedores_select(self):
        return supabase.table("proveedores_renting").select("id, nombre").execute().data

