from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from src.application.services.PersonService import PersonService
from src.infrastructure.repositories.person_repository_impl import PersonRepositoryImpl
from src.schemas.person import PersonCreate, PersonUpdate

router = APIRouter(tags=["Personas"])

# Inyección de dependencia
def get_person_service():
    return PersonService(PersonRepositoryImpl())

@router.get("/personas")
async def list_persons(search: Optional[str] = Query(None), service: PersonService = Depends(get_person_service)):
    return await service.get_all_persons(search)

@router.post("/personas")
async def create(data: PersonCreate, service: PersonService = Depends(get_person_service)):
    # .model_dump() de Pydantic v2 (o .dict() en v1)
    return await service.create_person(data.model_dump())

@router.put("/personas/{id}")
async def update(id: int, data: PersonUpdate, service: PersonService = Depends(get_person_service)):
    return await service.update_person(id, data.model_dump(exclude_unset=True))

@router.delete("/personas/{id}")
async def delete(id: int, service: PersonService = Depends(get_person_service)):
    return await service.delete_person(id)

@router.get("/areas")
async def areas(service: PersonService = Depends(get_person_service)):
    return await service.get_areas_list()