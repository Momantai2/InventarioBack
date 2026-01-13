from src.domain.exceptions import EntityNotFoundError, BusinessRuleError
from src.infrastructure.repositories.catalog_repository_impl import CatalogRepositoryImpl

class CatalogService:
    def __init__(self, repository: CatalogRepositoryImpl):
        self.repo = repository

    # --- Lógica de Marcas ---
    async def get_marcas(self):
        return self.repo.get_all_from_table("marcas")

    async def create_marca(self, data: dict):
        # Regla Senior: Estandarizar nombres a MAYÚSCULAS
        data["nombre"] = data["nombre"].upper()
        return self.repo.insert_into_table("marcas", data)

    # --- Lógica de Tipos de Equipo ---
    async def get_tipos_equipo(self):
        return self.repo.get_all_from_table("tipos_equipo")

    async def create_tipo_equipo(self, data: dict):
        data["nombre"] = data["nombre"].upper()
        return self.repo.insert_into_table("tipos_equipo", data)

    # --- Lógica de Modelos (Relacional) ---
    async def get_modelos(self):
        return self.repo.get_modelos_with_relations()

    async def create_modelo(self, data: dict):
        data["nombre"] = data["nombre"].upper()
        return self.repo.create_modelo_full(data)

    async def delete_item(self, table: str, item_id: int):
        try:
            return self.repo.delete_from_table(table, item_id)
        except Exception:
            # Capturamos error de restricción de llave foránea (equipo usando el modelo)
            raise BusinessRuleError(f"No se puede eliminar: el registro en '{table}' está siendo usado por otros equipos.")
    
    async def get_tipos_equipo(self):
        """Retorna todos los tipos de equipo ordenados alfabéticamente."""
        return self.repo.get_all_from_table("tipos_equipo")

    async def create_tipo_equipo(self, data: dict):
        """Crea un nuevo tipo de equipo (ej: LAPTOP) en mayúsculas."""
        print(f"DEBUG DATA: {data}")

    async def delete_tipo_equipo(self, tipo_id: int):
        """Elimina un tipo de equipo si no está en uso."""
        return self.repo.delete_from_table("tipos_equipo", tipo_id)