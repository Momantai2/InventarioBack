

from datetime import datetime
from src.domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError, BusinessRuleError
from src.infrastructure.repositories.insumos_repository_impl import InsumoRepositoryImpl

class InsumoService:
    def __init__(self, repository: InsumoRepositoryImpl):
        self.repo = repository

    async def list_insumos(self):
        return self.repo.get_all_insumos()

    async def add_insumo(self, data: dict):
    # 1. Normalizar el nombre para evitar "Toner" vs "toner "
     nombre_limpio = data["nombre"].strip()
     existente = self.repo.get_by_name(nombre_limpio)
    
     if existente:
         raise EntityAlreadyExistsError(f"Ya existe un insumo registrado como '{nombre_limpio}'")
    
     data["nombre"] = nombre_limpio
     return self.repo.create_insumo(data)

    async def modify_insumo(self, insumo_id: int, data: dict):
     nombre_nuevo = data["nombre"].strip()
    
     existente = self.repo.get_by_name(nombre_nuevo)
    
     if existente and existente["id"] != insumo_id:
        raise BusinessRuleError(f"El nombre '{nombre_nuevo}' ya está siendo usado por otro insumo.")
        
     data["nombre"] = nombre_nuevo
     return self.repo.update_insumo(insumo_id, data)

    async def remove_insumo(self, insumo_id: int):
        return self.repo.delete_insumo(insumo_id)
    
    #TABLA MOVIMIENTOS INSUMOS
    
    
    async def list_movimientos_insumos(self):
        return self.repo.get_all_movimientos_insumos()
    
    async def registrar_movimiento(self, data: dict):
        insumo = self.repo.get_insumo_by_id(data["insumo_id"])
        if not insumo:
            raise EntityNotFoundError("El insumo no existe")

        nuevo_total = insumo["stock_actual"] + data["cantidad"]
        if nuevo_total < 0:
            raise BusinessRuleError("No hay suficiente stock para esta salida.")

        self.repo.create_movement_log(data)
        return self.repo.update_stock_level(data["insumo_id"], nuevo_total)
    
    async def modify_movimiento_insumo(self, insumo_id: int, data: dict):
        return self.repo.update_movimientos_insumo(insumo_id, data)

    async def remove_movimiento_insumo(self, insumo_id: int):
        return self.repo.delete_movimientos_insumo(insumo_id)

    # NUEVA: Listar Alertas
    async def list_alertas_stock(self):
        return self.repo.get_low_stock_insumos()
    
    