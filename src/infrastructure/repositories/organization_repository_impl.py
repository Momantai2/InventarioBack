from src.infrastructure.supabase_client import supabase

class OrganizationRepositoryImpl:
    def __init__(self):
        pass

    def get_gerencias(self):
        return supabase.table("gerencias").select("*").order("nombre").execute().data

    def get_areas(self):
        return supabase.table("areas").select("*, gerencias(*)").order("nombre").execute().data

    def get_ubicaciones_detalladas(self):
        return supabase.table("ubicaciones_detalladas").select("""
            id, area_id, sede_id, piso_oficina,
            areas(*, gerencias(*)),
            sedes_agencias(*, departamentos(*), tipos_local(*))
        """).execute().data

    def create_ubicacion_detallada(self, data: dict):
        res = supabase.table("ubicaciones_detalladas").insert(data).execute()
        nuevo_id = res.data[0]['id']
        # Retornamos con relaciones para que el Front actualice su estado correctamente
        return supabase.table("ubicaciones_detalladas").select("""
            id, area_id, sede_id, piso_oficina,
            areas(*, gerencias(*)),
            sedes_agencias(*, departamentos(*), tipos_local(*))
        """).eq("id", nuevo_id).single().execute().data

    def exists_ubicacion(self, id: int) -> bool:
        res = supabase.table("ubicaciones_detalladas").select("id").eq("id", id).execute()
        return len(res.data) > 0

    def delete_ubicacion(self, id: int):
        return supabase.table("ubicaciones_detalladas").delete().eq("id", id).execute()

    def get_table_data(self, table_name: str):
        return supabase.table(table_name).select("*").order("nombre").execute().data
    
    # Añadir a la clase OrganizationRepositoryImpl

    def get_sedes_with_relations(self):
        """Trae sedes con sus departamentos y tipos de local asociados."""
        return supabase.table("sedes_agencias").select("""
            *, 
            departamentos(*), 
            tipos_local(*)
        """).order("nombre").execute().data

    def create_sede_full(self, data: dict):
        """Inserta una sede y la devuelve con sus objetos relacionados."""
        res = supabase.table("sedes_agencias").insert(data).execute()
        nuevo_id = res.data[0]['id']
        return supabase.table("sedes_agencias").select("""
            *, 
            departamentos(*), 
            tipos_local(*)
        """).eq("id", nuevo_id).single().execute().data