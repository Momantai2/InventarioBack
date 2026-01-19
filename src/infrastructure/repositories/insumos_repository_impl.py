from src.infrastructure.supabase_client import supabase


class InsumoRepositoryImpl:

# TABLA INSUMOS
    def get_all_insumos(self):
        return supabase.table("insumos")\
            .select("*, tipos_equipo(nombre)")\
            .eq("activo", True)\
            .order("nombre")\
            .execute().data
    # READ ONE
    def get_insumo_by_id(self, insumo_id: int):
        return supabase.table("insumos").select("*").eq("id", insumo_id).single().execute().data

    # CREATE
    def create_insumo(self, data: dict):
        result = supabase.table("insumos").insert(data).execute()
        return result.data[0]

    # UPDATE
    def update_insumo(self, insumo_id: int, data: dict):
        return supabase.table("insumos").update(data).eq("id", insumo_id).execute().data[0]

    # DELETE
    def delete_insumo(self, insumo_id: int):
        return supabase.table("insumos").update({"activo": False}).eq("id", insumo_id).execute()
    
    
    #TABLA HISOTRIAL INSUMOS
    
    def get_all_movimientos_insumos(self):
        return supabase.table("movimientos_insumos")\
            .select("*, insumos(nombre, tipo_equipo_id), personas(nombre_completo)")\
            .order("fecha", desc=True)\
            .execute().data

    def get_movimientos_insumo_by_id(self, insumo_id: int):
        return supabase.table("movimientos_insumos").select("*").eq("id", insumo_id).single().execute().data

    def create_movimientos_insumo(self, data: dict):
        result = supabase.table("movimientos_insumos").insert(data).execute()
        return result.data[0]

    def update_movimientos_insumo(self, insumo_id: int, data: dict):
        return supabase.table("movimientos_insumos").update(data).eq("id", insumo_id).execute().data[0]

    def delete_movimientos_insumo(self, insumo_id: int):
        return supabase.table("movimientos_insumos").delete().eq("id", insumo_id).execute()
    
    #FUNCIONES ESPECIALES
    def get_low_stock_insumos(self):
        # Filtramos donde stock_actual es menor o igual al minimo
        return supabase.table("insumos")\
            .select("*, tipos_equipo(nombre)")\
            .lte("stock_actual", "stock_minimo")\
            .execute().data

    # 2. Función para Actualizar Stock (Solo el número)
    def update_stock_level(self, insumo_id: int, nuevo_stock: int):
        return supabase.table("insumos")\
            .update({"stock_actual": nuevo_stock})\
            .eq("id", insumo_id)\
            .execute()

    # 3. Registrar el rastro en la tabla de movimientos
    def create_movement_log(self, data: dict):
        return supabase.table("movimientos_insumos").insert(data).execute()
    
    def get_movimientos_by_persona(self, persona_id: int):
         return supabase.table("movimientos_insumos")\
        .select("*, insumos(nombre)")\
        .eq("personal_id", persona_id)\
        .order("fecha", desc=True).execute().data
    
    def get_by_name(self, nombre: str):
    # .ilike hace una búsqueda insensible a mayúsculas/minúsculas
        result = supabase.table("insumos").select("*").ilike("nombre", nombre).execute()
        return result.data[0] if result.data else None