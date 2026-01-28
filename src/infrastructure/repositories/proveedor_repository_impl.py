from src.infrastructure.supabase_client import supabase

class ProveedorRepository:
    def get_all(self):
        return supabase.table("proveedores_renting").select("*").order("nombre").execute().data

    def create(self, data: dict):
        # Supabase acepta el formato ISO string que enviaremos desde el service
        result = supabase.table("proveedores_renting").insert(data).execute()
        return result.data[0]

    def delete(self, proveedor_id: int):
        return supabase.table("proveedores_renting").delete().eq("id", proveedor_id).execute()