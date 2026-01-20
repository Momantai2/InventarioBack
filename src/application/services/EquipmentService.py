from datetime import datetime
from src.domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError, BusinessRuleError
from src.infrastructure.repositories.equipment_repository_impl import EquipmentRepositoryImpl

class EquipmentService:
    def __init__(self, repository: EquipmentRepositoryImpl):
        self.repo = repository

    # --- Lógica de Equipos ---
    async def get_all_equipments(self, search: str = None):
        return self.repo.get_all(search)

    async def create_equipment(self, data: dict):
        if self.repo.exists_by_serie(data['serie']):
            raise EntityAlreadyExistsError(f"La serie '{data['serie']}' ya está registrada.")
        return self.repo.create_data(data)

    async def update_equipment(self, eq_id: int, updates: dict):
        # Validar si existe antes de editar
        if not self.repo.get_by_id(eq_id):
            raise EntityNotFoundError("Equipo no encontrado")
        
        # Validar serie duplicada si se está intentando cambiar
        if "serie" in updates:
            if self.repo.exists_by_serie(updates["serie"], exclude_id=eq_id):
                raise EntityAlreadyExistsError("La nueva serie ya pertenece a otro equipo.")
                
        return self.repo.update(eq_id, updates)

    async def delete_equipment(self, eq_id: int):
        return self.repo.delete(eq_id)

    # --- procesos
    
    async def check_serie_availability(self, serie: str, exclude_id: int = None) -> bool:
        
        if not serie or len(serie) < 3:
            return False
        return self.repo.exists_by_serie(serie, exclude_id)

    # --- Lógica de Catálogos formateados ---
    async def get_formatted_locations(self):
        raw_data = self.repo.get_locations_raw()
        return [
            {
                "id": u["id"], 
                "nombre": f"{u['sedes_agencias']['nombre']} - {u['areas']['nombre']} ({u['piso_oficina']})"
            } for u in raw_data
        ]

    async def get_formatted_models(self):
        raw_data = self.repo.get_models_raw()
        return [
            {"id": m["id"], "nombre": f"{m['marcas']['nombre']} - {m['nombre']}"} 
            for m in raw_data
        ]
        
    async def get_all_proveedores(self):
        """Retorna la lista completa de proveedores ordenada por nombre."""
        return self.repo.get_proveedores_renting()

    async def create_proveedor(self, data: dict):
        """Crea un nuevo proveedor de renting."""
        # Senior Tip: Podrías normalizar el nombre a mayúsculas aquí si lo deseas
        data["nombre"] = data["nombre"].upper()
        return self.repo.create_proveedor_renting(data)
    
    async def delete_proveedor(self, eq_id: int):
        return self.repo.delete(eq_id)

    async def get_proveedores_for_select(self):
        """Retorna solo ID y Nombre para dropdowns en el frontend."""
        return self.repo.get_proveedores_select()
    
    async def get_all_estados(self):
        """Retorna la lista de estados para el inventario."""
        return self.repo.get_estados()

    async def get_estado_by_id(self, estado_id: int):
        return self.repo.get_estado_by_id(estado_id)
    
    #modleos
    