from src.infrastructure.repositories.proveedor_repository_impl import ProveedorRepository

class ProveedorService:
    def __init__(self):
        self.repo = ProveedorRepository()

    async def list_proveedores(self):
        return self.repo.get_all()

    async def create_proveedor(self, data: dict):
        # Normalizamos el nombre a mayúsculas
        data["nombre"] = data["nombre"].upper()
        
        # Convertimos objetos date a strings para evitar conflictos de inserción
        if data.get("fecha_inicio_contrato"):
            data["fecha_inicio_contrato"] = str(data["fecha_inicio_contrato"])
        if data.get("fecha_vencimiento_contrato"):
            data["fecha_vencimiento_contrato"] = str(data["fecha_vencimiento_contrato"])
            
        return self.repo.create(data)

    async def delete_proveedor(self, proveedor_id: int):
        return self.repo.delete(proveedor_id)