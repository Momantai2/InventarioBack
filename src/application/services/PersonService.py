from typing import Optional
from src.schemas.person import PersonasCreate, PersonasUpdate, PersonaPagedResponse
from src.infrastructure.repositories.person_repository_impl import PersonRepositoryImpl
from src.infrastructure.repositories.organization_repository_impl import OrganizationRepositoryImpl

from src.api.errors import EntityNotFoundError, BusinessRuleError # Asumiendo tus excepciones personalizadas

class PersonService:
    def __init__(self):
        self.repo = PersonRepositoryImpl()
        self.repo1 = OrganizationRepositoryImpl()
    async def get_personas(self, query: Optional[str] = None, page: int = 1, page_size: int = 20) -> PersonaPagedResponse:
        """Obtiene la lista de personas con validación de rangos de página."""
        page = max(1, page)
        page_size = min(100, max(1, page_size))
        return self.repo.get_all_paginated(query=query, page=page, page_size=page_size)

    async def create_persona(self, data: PersonasCreate):
        """Crea una persona validando DNI único y existencia del área."""
        # 1. Validar que el Área exista (Integridad)
        # Nota: Usamos el repo de organización o el método get_area_by_id del repo de personas
        if not self.repo1.get_area_by_id(data.area_id):
            raise EntityNotFoundError(f"El Área con ID {data.area_id} no existe.")

        # 2. Validar DNI único
        if self.repo.exists_by_dni(data.dni):
            raise BusinessRuleError(f"Ya existe una persona registrada con el DNI {data.dni}.")

        # 3. Limpieza de datos
        data.nombre_completo = data.nombre_completo.strip().upper()
        data.dni = data.dni.strip()

        return self.repo.create(data.model_dump())

    async def update_persona(self, persona_id: int, data: PersonasUpdate):
        """Actualiza una persona validando existencia y conflictos de DNI."""
        persona_actual = self.repo.get_by_id(persona_id)
        if not persona_actual:
            raise EntityNotFoundError(f"Persona con ID {persona_id} no encontrada.")

        # 1. Si intenta cambiar de área, validar que la nueva exista
        if data.area_id and data.area_id != persona_actual["area_id"]:
            if not self.repo1.get_area_by_id(data.area_id):
                raise EntityNotFoundError(f"El Área especificada con ID {data.area_id} no existe.")

        # 2. Si intenta cambiar el DNI, validar que no esté en uso por otro
        if data.dni and data.dni != persona_actual["dni"]:
            if self.repo.exists_by_dni(data.dni, exclude_id=persona_id):
                raise BusinessRuleError(f"El DNI {data.dni} ya está asignado a otra persona.")

        # 3. Limpieza de strings si vienen en el update
        if data.nombre_completo:
            data.nombre_completo = data.nombre_completo.strip().upper()
        
        if data.dni:
            data.dni = data.dni.strip()

        return self.repo.update(persona_id, data.model_dump(exclude_unset=True))

    async def delete_persona(self, persona_id: int):
        """Eliminación lógica de persona validando activos vinculados."""
        if not self.repo.get_by_id(persona_id):
            raise EntityNotFoundError(f"Persona con ID {persona_id} no encontrada.")

        # REGLA DE ORO: No eliminar si es responsable de equipos físicos
        if self.repo.has_active_personas(persona_id):
            raise BusinessRuleError("No se puede eliminar: Esta persona tiene equipos vinculados bajo su responsabilidad.")

        # Marcamos como inactivo (Eliminación lógica)
        return self.repo.update(persona_id, {"activo": False})