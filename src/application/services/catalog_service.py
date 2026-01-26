from src.domain.exceptions import EntityNotFoundError, BusinessRuleError
from src.infrastructure.repositories.catalog_repository_impl import CatalogRepositoryImpl
from src.domain.exceptions import (
    EntityNotFoundError, 
    EntityAlreadyExistsError, 
    BusinessRuleError
)
from typing import Optional
from src.schemas.catalog import MarcaCreate,MarcaUpdate,TiposEquipoCreate,TiposEquipoUpdate,EstadoCreate,EstadoUpdate,ModelosCreate,ModelosUpdate

class CatalogService:
    def __init__(self, repository: CatalogRepositoryImpl):
        self.repo = repository
    #MARCAS


    async def get_marcas(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        page = max(1, page) 
        page_size = min(100, max(1, page_size)) 
    
        return self.repo.get_marcas(query=query, page=page, page_size=page_size)
    
    async def create_marca(self, data: MarcaCreate):
        data.nombre = data.nombre.strip().upper()

        if self.repo.get_marca_by_name(data.nombre):
            raise EntityAlreadyExistsError(f"La Marca '{data.nombre}' ya existe.")

        return self.repo.create_marca(data.model_dump())

    async def update_marca(self, marca_id: int, data: MarcaUpdate):
        marca_actual = self.repo.get_marca_by_id(marca_id)
        
        if not marca_actual:
            raise EntityNotFoundError(f"Marca con ID {marca_id} no encontrada.")

        if data.nombre:
            data.nombre = data.nombre.strip().upper()
            if data.nombre != marca_actual["nombre"]:
                if self.repo.get_marca_by_name(data.nombre):
                    raise EntityAlreadyExistsError("El nuevo nombre ya está en uso.")

        return self.repo.update_marca(marca_id, data.model_dump(exclude_unset=True))

    async def delete_marca(self, marca_id: int):
        if not self.repo.get_marca_by_id(marca_id):
            raise EntityNotFoundError("Marca no encontrada.")

        # Usamos BusinessRuleError para la integridad referencial
        if self.repo.has_active_marcas(marca_id):
            raise BusinessRuleError("No se puede eliminar: Esta marca tiene modelos activas.")

        return self.repo.update_marca(marca_id, {"activo": False})
    
    #TIPOS EQUIPO
    
    async def get_tipos_equipo(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        page = max(1, page) 
        page_size = min(100, max(1, page_size)) 
    
        return self.repo.get_tipos_equipo(query=query, page=page, page_size=page_size)
    
    async def create_tipo_equipo(self, data: TiposEquipoCreate):
        data.nombre = data.nombre.strip().upper()

        if self.repo.get_tipos_equipo_by_name(data.nombre):
            raise EntityAlreadyExistsError(f"El Tipo Equipo '{data.nombre}' ya existe.")

        return self.repo.create_tipos_equipo(data.model_dump())

    async def update_tipos_equipo(self, tipos_equipo_id: int, data: TiposEquipoUpdate):
        tipos_equipo_actual = self.repo.get_tipos_equipo_by_id(tipos_equipo_id)
        
        if not tipos_equipo_actual:
            raise EntityNotFoundError(f"Tipo Equipo  con ID {tipos_equipo_id} no encontrada.")

        if data.nombre:
            data.nombre = data.nombre.strip().upper()
            if data.nombre != tipos_equipo_actual["nombre"]:
                if self.repo.get_tipos_equipo_by_name(data.nombre):
                    raise EntityAlreadyExistsError("El nuevo nombre ya está en uso.")

        return self.repo.update_tipos_equipo(tipos_equipo_id, data.model_dump(exclude_unset=True))

    async def delete_tipos_equipo(self, tipo_equipo_id: int):
        if not self.repo.get_tipos_equipo_by_id(tipo_equipo_id):
            raise EntityNotFoundError("Tipo Equipo no encontrada.")

        # Usamos BusinessRuleError para la integridad referencial
        if self.repo.has_active_tipos_equipo(tipo_equipo_id):
            raise BusinessRuleError("No se puede eliminar: Este Tipo Equipo tiene modelos activos.")

        return self.repo.update_tipos_equipo(tipo_equipo_id, {"activo": False})
    
        #ESTADOS
        
    async def get_estados(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        page = max(1, page) 
        page_size = min(100, max(1, page_size)) 
    
        return self.repo.get_estados(query=query, page=page, page_size=page_size)
    
    async def create_estado(self, data: EstadoCreate):
        data.nombre = data.nombre.strip().upper()

        if self.repo.get_estados_by_name(data.nombre):
            raise EntityAlreadyExistsError(f"El Estado '{data.nombre}' ya existe.")

        return self.repo.create_estados(data.model_dump())

    async def update_estado(self, estados_id: int, data: EstadoCreate):
        estado_actual = self.repo.get_estados_by_id(estados_id)
        
        if not estado_actual:
            raise EntityNotFoundError(f"Estado  con ID {estados_id} no encontrada.")

        if data.nombre:
            data.nombre = data.nombre.strip().upper()
            if data.nombre != estado_actual["nombre"]:
                if self.repo.get_estados_by_name(data.nombre):
                    raise EntityAlreadyExistsError("El nuevo nombre ya está en uso.")

        return self.repo.update_estados(estados_id, data.model_dump(exclude_unset=True))

    async def delete_estado(self, estados_id: int):
        if not self.repo.get_estados_by_id(estados_id):
            raise EntityNotFoundError("Tipo Equipo no encontrada.")

        # Usamos BusinessRuleError para la integridad referencial
        if self.repo.has_active_estados(estados_id):
            raise BusinessRuleError("No se puede eliminar: Este Estado tiene equipos activos.")

        return self.repo.update_estados(estados_id, {"activo": False})
    
    #MODELOS
    
    async def get_modelos(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        page = max(1, page) 
        page_size = min(100, max(1, page_size)) 
    
        return self.repo.get_modelos(query=query, page=page, page_size=page_size)

    async def create_modelo(self, data: ModelosCreate):
        # 1. Validar que el Área exista
        if not self.repo.get_marca_by_id(data.marca_id):
            raise EntityNotFoundError(f"La Marca con ID {data.marca_id} no existe.")

        # 2. Validar que la Sede exista
        if not self.repo.get_tipos_equipo_by_id(data.tipo_equipo_id):
            raise EntityNotFoundError(f"El Tipo Equipo con ID {data.tipo_equipo_id} no existe.")

        data.nombre = data.nombre.strip().upper()

        return self.repo.create_modelo(data.model_dump())

    async def update_modelo(self, modelo_id: int, data: ModelosUpdate):
        modelo_actual = self.repo.get_modelo_by_id(modelo_id)
        if not modelo_actual:
            raise EntityNotFoundError(f"Ubicación con ID {modelo_id} no encontrada.")

        # Validaciones de integridad si se intenta cambiar IDs
        if data.marca_id and data.marca_id != modelo_actual["marca_id"]:
            if not self.repo.get_marca_by_id(data.marca_id):
                raise EntityNotFoundError("La Marca especificada no existe.")

        if data.tipo_equipo_id and data.tipo_equipo_id != modelo_actual["tipo_equipo_id"]:
            if not self.repo.get_tipos_equipo_by_id(data.tipo_equipo_id):
                raise EntityNotFoundError("El Tipo Equipo especificada no existe.")

        if data.nombre:
            data.nombre = data.nombre.strip().upper()

        return self.repo.update_modelo(modelo_id, data.model_dump(exclude_unset=True))

    async def delete_modelo(self, modelo_id: int):
        if not self.repo.get_modelo_by_id(modelo_id):
            raise EntityNotFoundError("modelo no encontrado.")

        # REGLA DE ORO: No desactivar si hay hardware físico ahí
        if self.repo.has_active_modelo(modelo_id):
            raise BusinessRuleError("No se puede eliminar: Hay equipos vinculados a esta modelo.")

        return self.repo.update_modelo(modelo_id, {"activo": False})