from src.domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from src.infrastructure.repositories.person_repository_impl import PersonRepositoryImpl

class PersonService:
    def __init__(self, repository: PersonRepositoryImpl):
        self.repo = repository

    async def get_all_persons(self, search: str = None):
        return self.repo.get_all(search)

    async def create_person(self, person_data: dict):
        # Lógica Senior: Validar DNI único antes de insertar
        dni = person_data.get("dni")
        if self.repo.exists_by_dni(dni):
            raise EntityAlreadyExistsError(f"El DNI {dni} ya se encuentra registrado.")
        
        return self.repo.create(person_data)

    async def update_person(self, person_id: int, updates: dict):
        # Verificar existencia
        existing = self.repo.get_by_id(person_id)
        if not existing:
            raise EntityNotFoundError("La persona no existe.")

        # Si cambia el DNI, validar que el nuevo no esté ocupado
        new_dni = updates.get("dni")
        if new_dni and new_dni != existing.get("dni"):
            if self.repo.exists_by_dni(new_dni, exclude_id=person_id):
                raise EntityAlreadyExistsError(f"El DNI {new_dni} ya pertenece a otra persona.")

        return self.repo.update(person_id, updates)

    async def delete_person(self, person_id: int):
        # Aquí podrías añadir lógica: ¿Se puede borrar si tiene equipos asignados?
        return self.repo.delete(person_id)

    async def get_areas_list(self):
        return self.repo.get_areas()