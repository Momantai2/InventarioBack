from src.infrastructure.supabase_client import supabase

class CatalogRepositoryImpl:
    def __init__(self):
        pass

    def get_all_from_table(self, table_name: str):
        return supabase.table(table_name).select("*").order("nombre").execute().data

    def insert_into_table(self, table_name: str, data: dict):
        res = supabase.table(table_name).insert(data).execute()
        return res.data[0] if res.data else None

    def delete_from_table(self, table_name: str, item_id: int):
        return supabase.table(table_name).delete().eq("id", item_id).execute()

    def get_modelos_with_relations(self):
        return supabase.table("modelos").select("""
            id, nombre, marca_id, tipo_equipo_id, 
            marcas!inner(id, nombre), 
            tipos_equipo!inner(id, nombre)
        """).order("nombre").execute().data

    def create_modelo_full(self, data: dict):
        res = supabase.table("modelos").insert(data).execute()
        nuevo_id = res.data[0]['id']
        # Retornamos el objeto con sus relaciones para el frontend
        return supabase.table("modelos").select("*, marcas(*), tipos_equipo(*)").eq("id", nuevo_id).single().execute().data