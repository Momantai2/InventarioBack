from src.domain.exceptions import (
    EntityNotFoundError, 
    EntityAlreadyExistsError, 
    BusinessRuleError
)
from src.schemas.organization import GerenciaCreate, GerenciaUpdate,AreaCreate,AreaUpdate,DepartamentosCreate,DepartamentosUpdate,TiposLocalCreate,TiposLocalUpdate,SedesAgenciasCreate,SedesAgenciasUpdate,UbicacionesDetalladasCreate,UbicacionesDetalladaUpdate
from typing import Optional
from src.infrastructure.repositories.organization_repository_impl import OrganizationRepositoryImpl
class OrganizationService:
    def __init__(self, repository: OrganizationRepositoryImpl):
        self.repo = repository

    async def get_gerencias(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        page = max(1, page) 
        page_size = min(100, max(1, page_size)) 
    
        return self.repo.get_gerencias(query=query, page=page, page_size=page_size)
    
    async def create_gerencia(self, data: GerenciaCreate):
        data.nombre = data.nombre.strip().upper()

        if self.repo.get_gerencia_by_name(data.nombre):
            raise EntityAlreadyExistsError(f"La gerencia '{data.nombre}' ya existe.")

        return self.repo.create_gerencia(data.model_dump())

    async def update_gerencia(self, gerencia_id: int, data: GerenciaUpdate):
        gerencia_actual = self.repo.get_gerencia_by_id(gerencia_id)
        
        if not gerencia_actual:
            raise EntityNotFoundError(f"Gerencia con ID {gerencia_id} no encontrada.")

        if data.nombre:
            data.nombre = data.nombre.strip().upper()
            if data.nombre != gerencia_actual["nombre"]:
                if self.repo.get_gerencia_by_name(data.nombre):
                    raise EntityAlreadyExistsError("El nuevo nombre ya está en uso.")

        return self.repo.update_gerencia(gerencia_id, data.model_dump(exclude_unset=True))

    async def delete_gerencia(self, gerencia_id: int):
        if not self.repo.get_gerencia_by_id(gerencia_id):
            raise EntityNotFoundError("Gerencia no encontrada.")

        # Usamos BusinessRuleError para la integridad referencial
        if self.repo.has_active_areas(gerencia_id):
            raise BusinessRuleError("No se puede eliminar: Esta gerencia tiene áreas activas.")

        return self.repo.update_gerencia(gerencia_id, {"activo": False})
    
    #AREAS
    async def get_areas(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        page = max(1, page)
        page_size = min(100, max(1, page_size))
        return self.repo.get_areas(query=query, page=page, page_size=page_size)

    async def create_area(self, data: AreaCreate):
        data.nombre = data.nombre.strip().upper()

        gerencia = self.repo.get_gerencia_by_id(data.gerencia_id)
        if not gerencia or not gerencia.get("activo"):
            raise EntityNotFoundError(f"No se puede crear el área: La Gerencia con ID {data.gerencia_id} no existe o está inactiva.")

        if self.repo.get_area_by_name(data.nombre):
            raise EntityAlreadyExistsError(f"El área '{data.nombre}' ya existe.")

        return self.repo.create_area(data.model_dump())

    async def update_area(self, area_id: int, data: AreaUpdate):
        area_actual = self.repo.get_area_by_id(area_id)
        if not area_actual:
            raise EntityNotFoundError(f"Área con ID {area_id} no encontrada.")

        if data.gerencia_id and data.gerencia_id != area_actual["gerencia_id"]:
            if not self.repo.get_gerencia_by_id(data.gerencia_id):
                raise EntityNotFoundError(f"La Gerencia con ID {data.gerencia_id} no existe.")

        if data.nombre:
            data.nombre = data.nombre.strip().upper()
            if data.nombre != area_actual["nombre"]:
                if self.repo.get_area_by_name(data.nombre):
                    raise EntityAlreadyExistsError(f"El nombre '{data.nombre}' ya está en uso por otra área.")

        return self.repo.update_area(area_id, data.model_dump(exclude_unset=True))

    async def delete_area(self, area_id: int):
        if not self.repo.get_area_by_id(area_id):
            raise EntityNotFoundError("Área no encontrada.")

        if self.repo.has_active_area(area_id): 
            raise BusinessRuleError("No se puede eliminar: Esta área tiene ubicaciones físicas vinculadas.")

        return self.repo.update_area(area_id, {"activo": False})
    
    #DEPARTAMENTOS
    async def get_departamentos(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        page = max(1, page) 
        page_size = min(100, max(1, page_size)) 
    
        return self.repo.get_departamentos(query=query, page=page, page_size=page_size)
    
    async def create_departamento(self, data: DepartamentosCreate):
        data.nombre = data.nombre.strip().upper()

        if self.repo.get_departamento_by_name(data.nombre):
            raise EntityAlreadyExistsError(f"El Departamento '{data.nombre}' ya existe.")

        return self.repo.create_departamento(data.model_dump())

    async def update_departamento(self, departamento_id: int, data: DepartamentosUpdate):
        departamento_actual = self.repo.get_departamento_by_id(departamento_id)
        
        if not departamento_actual:
            raise EntityNotFoundError(f"Departamento con ID {departamento_id} no encontrada.")

        if data.nombre:
            data.nombre = data.nombre.strip().upper()
            if data.nombre != departamento_actual["nombre"]:
                if self.repo.get_departamento_by_name(data.nombre):
                    raise EntityAlreadyExistsError("El nuevo nombre ya está en uso.")

        return self.repo.update_departamento(departamento_id, data.model_dump(exclude_unset=True))

    async def delete_departamento(self, departamento_id: int):
        if not self.repo.get_departamento_by_id(departamento_id):
            raise EntityNotFoundError("Departamento no encontrada.")

        if self.repo.has_active_departamento(departamento_id):
            raise BusinessRuleError("No se puede eliminar: Este Departamento tiene sedes activas.")

        return self.repo.update_departamento(departamento_id, {"activo": False})
    
    #TIPOS LOCAL
    async def get_tipos_local(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        page = max(1, page) 
        page_size = min(100, max(1, page_size)) 
    
        return self.repo.get_tipos_local(query=query, page=page, page_size=page_size)
    
    async def create_tipos_local(self, data: TiposLocalCreate):
        data.nombre = data.nombre.strip().upper()

        if self.repo.get_tipo_local_by_name(data.nombre):
            raise EntityAlreadyExistsError(f"El Tipo Local '{data.nombre}' ya existe.")

        return self.repo.create_tipo_local(data.model_dump())

    async def update_tipos_local(self, tipo_local_id: int, data: TiposLocalUpdate):
        tipo_local_actual = self.repo.get_tipo_local_by_id(tipo_local_id)
        
        if not tipo_local_actual:
            raise EntityNotFoundError(f"Tipo Local con ID {tipo_local_id} no encontrada.")

        if data.nombre:
            data.nombre = data.nombre.strip().upper()
            if data.nombre != tipo_local_actual["nombre"]:
                if self.repo.get_tipo_local_by_name(data.nombre):
                    raise EntityAlreadyExistsError("El nuevo nombre ya está en uso.")

        return self.repo.update_tipo_local(tipo_local_id, data.model_dump(exclude_unset=True))

    async def delete_tipos_local(self, tipo_local_id: int):
        if not self.repo.get_tipo_local_by_id(tipo_local_id):
            raise EntityNotFoundError("Tipo Local no encontrado.")

        if self.repo.has_active_tipo_local(tipo_local_id):
            raise BusinessRuleError("No se puede eliminar: Este Tipo local tiene sedes activas.")

        return self.repo.update_tipo_local(tipo_local_id, {"activo": False})
    
    async def get_sedes_agencias(self, query: Optional[str] = None, page: int = 1, page_size: int = 20):
        page = max(1, page)
        page_size = min(100, max(1, page_size))
        return self.repo.get_sedes_agencias(query=query, page=page, page_size=page_size)

    async def create_sede_agencia(self, data: SedesAgenciasCreate):
        # 1. Estandarización
        data.nombre = data.nombre.strip().upper()

        # 2. Validar Departamento
        if not self.repo.get_departamento_by_id(data.departamento_id):
            raise EntityNotFoundError(f"El Departamento con ID {data.departamento_id} no existe.")

        # 3. Validar Tipo de Local
        if not self.repo.get_tipo_local_by_id(data.tipo_local_id):
            raise EntityNotFoundError(f"El Tipo de Local con ID {data.tipo_local_id} no existe.")

        # 4. Validar nombre duplicado
        if self.repo.get_sede_agencia_by_name(data.nombre):
            raise EntityAlreadyExistsError(f"La Sede/Agencia '{data.nombre}' ya existe.")

        return self.repo.create_sede_agencia(data.model_dump())

    async def update_sede_agencia(self, sede_id: int, data: SedesAgenciasUpdate):
        sede_actual = self.repo.get_sede_agencia_by_id(sede_id)
        if not sede_actual:
            raise EntityNotFoundError(f"Sede/Agencia con ID {sede_id} no encontrada.")

        # Validaciones de llaves foráneas si vienen en el patch
        if data.departamento_id and data.departamento_id != sede_actual["departamento_id"]:
            if not self.repo.get_departamento_by_id(data.departamento_id):
                raise EntityNotFoundError("El Departamento especificado no existe.")

        if data.tipo_local_id and data.tipo_local_id != sede_actual["tipo_local_id"]:
            if not self.repo.get_tipo_local_by_id(data.tipo_local_id):
                raise EntityNotFoundError("El Tipo de Local especificado no existe.")

        if data.nombre:
            data.nombre = data.nombre.strip().upper()
            if data.nombre != sede_actual["nombre"]:
                if self.repo.get_sede_agencia_by_name(data.nombre):
                    raise EntityAlreadyExistsError("El nuevo nombre ya está en uso.")

        return self.repo.update_sede_agencia(sede_id, data.model_dump(exclude_unset=True))

    async def delete_sede_agencia(self, sede_id: int):
        if not self.repo.get_sede_agencia_by_id(sede_id):
            raise EntityNotFoundError("Sede no encontrada.")

        # Validar si tiene ubicaciones detalladas (pisos/oficinas) vinculadas
        if self.repo.has_active_sede_agencia(sede_id):
            raise BusinessRuleError("No se puede eliminar: Esta sede tiene oficinas o pisos registrados.")

        return self.repo.update_sede_agencia(sede_id, {"activo": False})
    
    async def get_ubicaciones_detalladas(self, page: int = 1, page_size: int = 20):
        # En ubicaciones no solemos usar "query" por nombre porque no tienen campo nombre, 
        # pero podrías filtrar por área_id o sede_id en el futuro.
        page = max(1, page)
        page_size = min(100, max(1, page_size))
        return self.repo.get_ubicaciones_detalladas(page=page, page_size=page_size)

    async def create_ubicacion_detallada(self, data: UbicacionesDetalladasCreate):
        # 1. Validar que el Área exista
        if not self.repo.get_area_by_id(data.area_id):
            raise EntityNotFoundError(f"El Área con ID {data.area_id} no existe.")

        # 2. Validar que la Sede exista
        if not self.repo.get_sede_agencia_by_id(data.sede_id):
            raise EntityNotFoundError(f"La Sede con ID {data.sede_id} no existe.")

        # 3. Limpieza del campo piso_oficina
        data.piso_oficina = data.piso_oficina.strip().upper()

        return self.repo.create_ubicacion_detallada(data.model_dump())

    async def update_ubicacion_detallada(self, ubicacion_id: int, data: UbicacionesDetalladaUpdate):
        ubicacion_actual = self.repo.get_ubicacion_detallada_by_id(ubicacion_id)
        if not ubicacion_actual:
            raise EntityNotFoundError(f"Ubicación con ID {ubicacion_id} no encontrada.")

        # Validaciones de integridad si se intenta cambiar IDs
        if data.area_id and data.area_id != ubicacion_actual["area_id"]:
            if not self.repo.get_area_by_id(data.area_id):
                raise EntityNotFoundError("El Área especificada no existe.")

        if data.sede_id and data.sede_id != ubicacion_actual["sede_id"]:
            if not self.repo.get_sede_agencia_by_id(data.sede_id):
                raise EntityNotFoundError("La Sede especificada no existe.")

        if data.piso_oficina:
            data.piso_oficina = data.piso_oficina.strip().upper()

        return self.repo.update_ubicacion_detallada(ubicacion_id, data.model_dump(exclude_unset=True))

    async def delete_ubicacion_detallada(self, ubicacion_id: int):
        if not self.repo.get_ubicacion_detallada_by_id(ubicacion_id):
            raise EntityNotFoundError("Ubicación no encontrada.")

        # REGLA DE ORO: No desactivar si hay hardware físico ahí
        if self.repo.has_active_ubicacion_detallada(ubicacion_id):
            raise BusinessRuleError("No se puede eliminar: Hay equipos vinculados a esta ubicación.")

        return self.repo.update_ubicacion_detallada(ubicacion_id, {"activo": False})