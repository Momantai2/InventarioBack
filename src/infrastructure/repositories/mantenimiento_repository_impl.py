from src.infrastructure.supabase_client import supabase

class MantenimientoRepositoryImpl:
    def create(self, data: dict):
        
        res = supabase.table("mantenimientos").insert(data).execute()
    # Retornamos los datos directamente
        return res.data[0] if res.data else None

    def get_by_equipo(self, equipo_id: int):
    # El error suele estar en la cadena del .select()
    # Verifica que 'tipos_mantenimiento' sea el nombre exacto en Supabase
     return supabase.table("mantenimientos")\
        .select("*, tipos_mantenimiento(nombre)")\
        .eq("equipo_id", equipo_id)\
        .order("fecha_inicio", desc=True)\
        .execute().data

    def update(self, mant_id: int, data: dict):
         res = supabase.table("mantenimientos").update(data).eq("id", mant_id).execute()
    # Retornamos solo el primer registro de la lista de datos
         return res.data[0] if res.data else None
    
    def get_all(self):
        res = supabase.table("mantenimientos")\
            .select("*, tipos_mantenimiento(nombre), equipos(serie)")\
            .order("fecha_inicio", desc=True)\
        .   execute()
    
    # Normalizamos los datos para que el frontend reciba 'equipo_serie' directamente
        data = []
        for m in res.data:
             m['equipo_serie'] = m.get('equipos', {}).get('serie', 'N/A')
             data.append(m)
        
        return data
    
    def get_all_tipo_mantenimiento(self):
        return supabase.table("tipos_mantenimiento").select("*").order("id").execute().data

    def get_by_id_tipo_mantenimiento(self, tipo_id: int):
        return supabase.table("tipos_mantenimiento").select("*").eq("id", tipo_id).single().execute().data

    def create_tipo_mantenimiento(self, data: dict):
        return supabase.table("tipos_mantenimiento").insert(data).execute()

    def update_tipo_mantenimiento(self, tipo_id: int, data: dict):
        return supabase.table("tipos_mantenimiento").update(data).eq("id", tipo_id).execute()

    def delete_tipo_mantenimiento(self, tipo_id: int):
        return supabase.table("tipos_mantenimiento").delete().eq("id", tipo_id).execute()