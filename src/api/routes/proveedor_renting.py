from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.proveedor_renting import ProveedorRentingCreate, ProveedorRentingRead
from src.application.services.ProveedorService import ProveedorService

router = APIRouter(prefix="/proveedores", tags=["Proveedores de Renting"])
service = ProveedorService()

@router.get("/", response_model=List[ProveedorRentingRead])
async def get_proveedores():
    return await service.list_proveedores()

@router.post("/", response_model=ProveedorRentingRead)
async def create_proveedor(data: ProveedorRentingCreate):
    try:
        return await service.create_proveedor(data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{proveedor_id}")
async def delete_proveedor(proveedor_id: int):
    await service.delete_proveedor(proveedor_id)
    return {"message": "Proveedor eliminado correctamente"}