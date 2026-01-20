from datetime import date
from src.domain.exceptions import EntityNotFoundError,BadRequestError
class MantenimientoService:
    def __init__(self, mant_repo, eq_repo):
        self.mant_repo = mant_repo
        self.eq_repo = eq_repo

    async def register_entry(self, data: dict):
    # 1. Verificar existencia del equipo
        equipo = self.eq_repo.get_by_id(data['equipo_id'])
        if not equipo: 
            raise EntityNotFoundError("Equipo no encontrado")

        if data.get('fecha_inicio'):
            data['fecha_inicio'] = data['fecha_inicio'].isoformat()
    
        if data.get('proximo_mantenimiento'):
            data['proximo_mantenimiento'] = data['proximo_mantenimiento'].isoformat()
    
        if data.get('fecha_fin'):
         data['fecha_fin'] = data['fecha_fin'].isoformat()
    # -----------------------------------

    # 2. Cambiar equipo a estado MANTENIMIENTO (ID: 3)
        self.eq_repo.update(data['equipo_id'], {
            "estado_id": 3,
            "personal_usuario_id": None 
    })
        return self.mant_repo.create(data)

    async def register_exit(self, mant_id: int, equipo_id: int, exit_data: dict):
    # Convertimos fecha_fin a string ISO si es un objeto date
        if 'fecha_fin' in exit_data and not isinstance(exit_data['fecha_fin'], str):
            exit_data['fecha_fin'] = exit_data['fecha_fin'].isoformat()
    
    # 1. Cerrar registro de mantenimiento
        self.mant_repo.update(mant_id, exit_data)

    # 2. Cambiar equipo a estado DISPONIBLE (ID: 1)
        return self.eq_repo.update(equipo_id, {
        "estado_id": 1,
        "fecha_devolucion": exit_data['fecha_fin']
    })
    
    async def list_mantenimientos(self):
        return self.mant_repo.get_all()
    
    #TIPO MANTENIMIENTO
    async def list_all_tipo_mantenimiento(self):
        # Cambiado self.repo -> self.mant_repo 
        # Cambiado get_all -> get_all_tipo_mantenimiento
        return self.mant_repo.get_all_tipo_mantenimiento()

    async def get_one_tipo_mantenimiento(self, tipo_id: int):
        # Cambiado self.repo -> self.mant_repo
        # Cambiado get_by_id -> get_by_id_tipo_mantenimiento
        tipo = self.mant_repo.get_by_id_tipo_mantenimiento(tipo_id)
        if not tipo:
            raise EntityNotFoundError(f"ID {tipo_id} no encontrado")
        return tipo

    async def create_new_tipo_mantenimiento(self, data: dict):
        try:
            # Cambiado create -> create_tipo_mantenimiento
            res = self.mant_repo.create_tipo_mantenimiento(data)
            return res.data[0]
        except Exception as e:
            raise BadRequestError(f"Error: {str(e)}")

    async def update_existing_tipo_mantenimiento(self, tipo_id: int, data: dict):
        # Usar el nombre de método corregido arriba
        await self.get_one_tipo_mantenimiento(tipo_id)
        # Cambiado update -> update_tipo_mantenimiento
        res = self.mant_repo.update_tipo_mantenimiento(tipo_id, data)
        return res.data[0]

    async def remove_tipo_mantenimiento(self, tipo_id: int):
        await self.get_one_tipo_mantenimiento(tipo_id)
        # Cambiado delete -> delete_tipo_mantenimiento
        self.mant_repo.delete_tipo_mantenimiento(tipo_id)
        return {"status": "success", "message": "Registro eliminado"}