from datetime import datetime
from src.domain.exceptions import BusinessRuleError, EntityNotFoundError

class HistorialAsignacionesService:
    def __init__(self, historial_repo, equipment_repo):
        self.hist_repo = historial_repo
        self.eq_repo = equipment_repo

    async def assign_equipment(self, equipo_id: int, persona_id: int, tipo_movimiento_id: int, obs: str = None):
        """Asigna un equipo disponible a una persona (ID: 1)."""
        ahora = datetime.now()
        equipo = self.eq_repo.get_by_id(equipo_id)
        
        if not equipo: 
            raise EntityNotFoundError("Equipo no encontrado")
        if equipo.get("estado_id") == 4: 
            raise BusinessRuleError("No se puede asignar un equipo que está en BAJA")

        # 1. Cerrar asignación anterior si existe (Auditoría)
        activa = self.hist_repo.get_active_by_equipo(equipo_id)
        if activa:
            self.hist_repo.close_assignment(activa["id"], ahora)

        # 2. Crear registro de ASIGNACIÓN en historial
        hist_data = {
            "equipo_id": equipo_id,
            "persona_id": persona_id,
            "tipo_movimiento_id": tipo_movimiento_id, # Generalmente ID: 1
            "fecha_inicio": ahora.isoformat(),
            "observaciones": obs
        }
        nuevo_historial = self.hist_repo.create_historial(hist_data)

        # 3. Actualizar estado actual en tabla equipos
        self.eq_repo.update(equipo_id, {
            "personal_usuario_id": persona_id,
            "estado_id": 2, # ASIGNADO
            "fecha_asignacion": ahora.strftime("%Y-%m-%d")
        })
        return nuevo_historial

    async def release_equipment(self, equipo_id: int, obs: str = "Devolución de equipo a almacén"):
        """Libera un equipo y registra la DEVOLUCIÓN (ID: 2)."""
        ahora = datetime.now()
        equipo = self.eq_repo.get_by_id(equipo_id)
        
        if not equipo: 
            raise EntityNotFoundError("Equipo no encontrado")
        
        persona_que_devuelve = equipo.get("personal_usuario_id")

        # 1. Cerrar la asignación actual en historial
        activa = self.hist_repo.get_active_by_equipo(equipo_id)
        if activa:
            self.hist_repo.close_assignment(activa["id"], ahora)

        # 2. Crear registro explícito de DEVOLUCIÓN (Trazabilidad)
        if persona_que_devuelve:
            devolucion_data = {
                "equipo_id": equipo_id,
                "persona_id": persona_que_devuelve,
                "tipo_movimiento_id": 2, # DEVOLUCIÓN
                "fecha_inicio": ahora.isoformat(),
                "fecha_fin": ahora.isoformat(), # Evento puntual
                "observaciones": obs
            }
            self.hist_repo.create_historial(devolucion_data)

        # 3. Resetear equipo a DISPONIBLE
        return self.eq_repo.update(equipo_id, {
            "personal_usuario_id": None,
            "estado_id": 1, # DISPONIBLE
            "fecha_devolucion": ahora.strftime("%Y-%m-%d"),
            "fecha_asignacion": None
        })
    
    async def transfer_equipment(self, equipo_id: int, nuevo_persona_id: int, obs: str = None):
        """Transfiere el equipo directamente entre usuarios (ID: 3)."""
        ahora = datetime.now()
        equipo = self.eq_repo.get_by_id(equipo_id)
    
        if not equipo: 
            raise EntityNotFoundError("Equipo no encontrado")
    
        persona_anterior_id = equipo.get("personal_usuario_id")
        if not persona_anterior_id:
            raise BusinessRuleError("No se puede transferir un equipo que no está asignado. Use 'Asignar'.")

        # 1. Cerrar la posesión del usuario actual
        activa = self.hist_repo.get_active_by_equipo(equipo_id)
        if activa:
            self.hist_repo.close_assignment(activa["id"], ahora)

        # 2. Crear registro de TRANSFERENCIA
        transferencia_data = {
            "equipo_id": equipo_id,
            "persona_id": nuevo_persona_id,
            "tipo_movimiento_id": 3, # TRANSFERENCIA
            "fecha_inicio": ahora.isoformat(),
            "observaciones": f"Transferido desde ID {persona_anterior_id}. {obs or ''}"
        }
        self.hist_repo.create_historial(transferencia_data)

        # 3. Actualizar tabla equipos manteniendo rastro anterior
        return self.eq_repo.update(equipo_id, {
            "personal_usuario_id": nuevo_persona_id,
            "personal_anterior_id": persona_anterior_id,
            "estado_id": 2, 
            "fecha_asignacion": ahora.strftime("%Y-%m-%d")
        })

    async def decommission_equipment(self, equipo_id: int, obs: str = "Baja definitiva del activo"):
        """Retira el equipo de circulación por daño o vejez (ID: 4)."""
        ahora = datetime.now()
        equipo = self.eq_repo.get_by_id(equipo_id)

        if not equipo:
            raise EntityNotFoundError("Equipo no encontrado")

        # 1. Cerrar cualquier asignación activa antes de dar la baja
        activa = self.hist_repo.get_active_by_equipo(equipo_id)
        if activa:
            self.hist_repo.close_assignment(activa["id"], ahora)

        # 2. Registrar la BAJA en el historial
        baja_data = {
            "equipo_id": equipo_id,
            "persona_id": equipo.get("personal_usuario_id"), # Puede ser None
            "tipo_movimiento_id": 4, # BAJA
            "fecha_inicio": ahora.isoformat(),
            "fecha_fin": ahora.isoformat(),
            "observaciones": obs
        }
        self.hist_repo.create_historial(baja_data)

        # 3. Marcar equipo como inoperativo y desasignado
        return self.eq_repo.update(equipo_id, {
            "personal_usuario_id": None,
            "estado_id": 4, # ESTADO BAJA / INOPERATIVO
            "observaciones": f"BAJA REGISTRADA EL {ahora.date()}. {obs}"
        })

    async def list_all_history(self):
        """Obtiene la bitácora completa de movimientos."""
        return self.hist_repo.get_all_historial()

    async def get_history_by_equipment(self, equipo_id: int):   
        """Obtiene la línea de tiempo de un activo específico."""
        return self.hist_repo.get_by_equipo(equipo_id)
    
    async def bulk_assign(self, equipo_ids: list[int], persona_id: int, tipo_movimiento_id: int):
        """Asignación masiva de múltiples activos a una persona."""
        results = []
        for eq_id in equipo_ids:
            res = await self.assign_equipment(
                equipo_id=eq_id, 
                persona_id=persona_id, 
                tipo_movimiento_id=tipo_movimiento_id,
                obs="Asignación masiva de inventario"
            )
            results.append(res)
        return results