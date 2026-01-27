from datetime import datetime
from typing import Optional
from src.domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError, BusinessRuleError
from src.infrastructure.repositories.equipment_repository_impl import EquipmentRepositoryImpl
from src.schemas.inventory import EquipmentCreate

class EquipmentService:
    def __init__(self, repository: EquipmentRepositoryImpl):
        self.repo = repository

    # --- Lógica de Equipos con Paginación ---
    async def get_all_equipments(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        """Llama al repositorio paginado asegurando límites de página."""
        page = max(1, page)
        page_size = min(100, max(1, page_size))
        return self.repo.get_all_paginated(query, page, page_size)

    async def create_equipment(self, data: dict):
        """Registra un equipo con normalización y reglas de negocio."""
        # 1. Normalización
        data['serie'] = data['serie'].strip().upper()
        
        # 2. Validación de existencia
        if self.repo.exists_by_serie(data['serie']):
            raise EntityAlreadyExistsError(f"La serie '{data['serie']}' ya está registrada.")
        
        # 3. Regla de Negocio: Gestión Automática de Estados
        # Si se asigna un usuario al crear, el estado debe ser 'Asignado' (ID 2)
        # Si no hay usuario, el estado suele ser 'Stock' (ID 1)
        if data.get('personal_usuario_id'):
            data['estado_id'] = 2  
            data['fecha_asignacion'] = datetime.now().strftime("%Y-%m-%d")
        else:
            data['estado_id'] = 1

        return self.repo.create_data(data)

    async def update_equipment(self, eq_id: int, updates: dict):
        """Actualiza el equipo y gestiona cambios de responsable."""
        # 1. Verificar existencia
        current = self.repo.get_by_id(eq_id)
        if not current:
            raise EntityNotFoundError("Equipo no encontrado")
        
        # 2. Validar serie si cambia
        if "serie" in updates:
            updates["serie"] = updates["serie"].strip().upper()
            if self.repo.exists_by_serie(updates["serie"], exclude_id=eq_id):
                raise EntityAlreadyExistsError("La nueva serie ya pertenece a otro equipo.")
        
        # 3. Lógica de Trazabilidad (Anterior vs Actual)
        # Si estamos cambiando el usuario, movemos el actual al campo 'personal_anterior_id'
        if "personal_usuario_id" in updates:
            new_user = updates["personal_usuario_id"]
            if new_user != current["personal_usuario_id"]:
                updates["personal_anterior_id"] = current["personal_usuario_id"]
                updates["fecha_asignacion"] = datetime.now().strftime("%Y-%m-%d")
                # Si el nuevo usuario es None, el estado vuelve a Stock (1), sino Asignado (2)
                updates["estado_id"] = 2 if new_user else 1

        return self.repo.update(eq_id, updates)

    async def delete_equipment(self, eq_id: int):
        """Elimina físicamente el equipo (o podrías aplicar eliminación lógica)."""
        if not self.repo.get_by_id(eq_id):
            raise EntityNotFoundError("Equipo no encontrado")
        return self.repo.delete(eq_id)

    # --- Catálogos Formateados para Selects (Dropdowns) ---
    
    async def get_formatted_locations(self):
        """Retorna ubicaciones legibles: 'Sede - Área (Piso)'."""
        raw_data = self.repo.get_ubicaciones_for_select()
        return [
            {
                "id": u["id"], 
                "nombre": f"{u['sedes_agencias']['nombre']} - {u['areas']['nombre']} ({u['piso_oficina']})"
            } for u in raw_data
        ]

    async def get_formatted_models(self):
        """Retorna modelos legibles: 'Marca - Modelo'."""
        raw_data = self.repo.get_modelos_for_select()
        return [
            {
                "id": m["id"], 
                "nombre": f"{m['marcas']['nombre']} - {m['nombre']}"
            } for m in raw_data
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
    