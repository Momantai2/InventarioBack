from typing import List, Dict, Any
from src.infrastructure.supabase_client import supabase
from src.domain.entities.equipment import Equipment

class EquipmentRepositoryImpl:
    def __init__(self):
        self.table = "equipos"

    def create(self, equipment: Equipment) -> Dict[str, Any]:
        # Convertimos la entidad de dominio a un diccionario para Supabase
        data = {
            "serie": equipment.serie,
            "modelo_id": equipment.modelo_id,
            "estado_id": equipment.estado_id,
            "ubicacion_id": equipment.ubicacion_id,
            "proveedor_id": equipment.proveedor_id,
            "personal_usuario_id": equipment.personal_usuario_id,
            "specs": equipment.specs or {},
            "observaciones": equipment.observaciones
        }
        
        result = supabase.table(self.table).insert(data).execute()
        return result.data[0]

    def get_all(self):
        # Usamos la potencia de PostgREST (Supabase) para traer datos relacionados en una sola consulta
        query = """
            *,
            modelos (
                nombre,
                marcas (nombre),
                tipos_equipo (nombre)
            ),
            estados (nombre),
            ubicaciones_detalladas (
                piso_oficina,
                sedes_agencias (nombre),
                areas (nombre)
            ),
            personas:personal_usuario_id (nombre_completo)
        """
        result = supabase.table(self.table).select(query).execute()
        return result.data
    def update(self, equipment_id: int, data: dict):
        result = supabase.table(self.table).update(data).eq("id", equipment_id).execute()
        return result.data[0]

    def delete(self, equipment_id: int):
        supabase.table(self.table).delete().eq("id", equipment_id).execute()
        return {"status": "deleted"}
    
    def exists_by_serie(self, serie: str, exclude_id: int = None) -> bool:
        query = supabase.table(self.table).select("id").eq("serie", serie)
        
        # Si estamos editando, ignoramos el ID del equipo actual
        if exclude_id:
            query = query.neq("id", exclude_id)
            
        result = query.execute()
        return len(result.data) > 0    