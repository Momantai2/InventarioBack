from src.domain.exceptions import EntityNotFoundError
from src.infrastructure.repositories.organization_repository_impl import OrganizationRepositoryImpl

class OrganizationService:
    def __init__(self, repository: OrganizationRepositoryImpl):
        self.repo = repository

    # --- Lógica de Estructura ---
    async def get_all_gerencias(self):
        return self.repo.get_gerencias()

    async def get_all_areas(self):
        return self.repo.get_areas()

    # --- Lógica de Ubicaciones ---
    async def get_ubicaciones_detalladas(self):
        return self.repo.get_ubicaciones_detalladas()

    async def create_ubicacion_detallada(self, data: dict):
        # El servicio se asegura de devolver el objeto completo tras insertar
        return self.repo.create_ubicacion_detallada(data)

    async def delete_ubicacion(self, id: int):
        if not self.repo.exists_ubicacion(id):
            raise EntityNotFoundError("La ubicación no existe.")
        return self.repo.delete_ubicacion(id)

    # Métodos genéricos para catálogos simples
    async def get_departamentos(self):
        return self.repo.get_table_data("departamentos")

    async def get_tipos_local(self):
        return self.repo.get_table_data("tipos_local")
    
    async def get_sedes(self):
        return self.repo.get_sedes_with_relations()

    async def create_sede(self, data: dict):
        # Estandarizamos el nombre a MAYÚSCULAS
        data["nombre"] = data["nombre"].upper()
        return self.repo.create_sede_full(data)