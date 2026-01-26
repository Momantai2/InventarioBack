from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from src.schemas.person import PersonasCreate, PersonasUpdate, PersonasRead, PersonaPagedResponse
from src.application.services.PersonService import PersonService

router = APIRouter(prefix="/personas", tags=["Personas"])

def get_person_service():
    return PersonService()

@router.get("/", response_model=PersonaPagedResponse)
async def get_personas(
    query: Optional[str] = Query(None, description="Buscar por nombre o DNI"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: PersonService = Depends(get_person_service)
):
    return await service.get_personas(query=query, page=page, page_size=page_size)

@router.post("/", response_model=PersonasRead, status_code=status.HTTP_201_CREATED)
async def create_persona(
    data: PersonasCreate,
    service: PersonService = Depends(get_person_service)
):
    return await service.create_persona(data)

@router.patch("/{persona_id}", response_model=PersonasRead)
async def update_persona(
    persona_id: int,
    data: PersonasUpdate,
    service: PersonService = Depends(get_person_service)
):
    return await service.update_persona(persona_id, data)

@router.delete("/{persona_id}", status_code=status.HTTP_200_OK)
async def delete_persona(
    persona_id: int,
    service: PersonService = Depends(get_person_service)
):
    return await service.delete_persona(persona_id)