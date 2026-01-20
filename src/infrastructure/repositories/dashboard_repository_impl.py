class DashboardService:
    def __init__(self, eq_repo, hist_repo):
        self.eq_repo = eq_repo
        self.hist_repo = hist_repo

    async def get_overview_stats(self):
        equipos = self.eq_repo.get_all() # Reutilizamos tu consulta pesada
        
        # Lógica de procesamiento en Python (muy rápida para miles de registros)
        total = len(equipos)
        
        # Contar por estado
        estados_count = {}
        for eq in equipos:
            nombre_estado = eq.get('estados', {}).get('nombre', 'Desconocido')
            estados_count[nombre_estado] = estados_count.get(nombre_estado, 0) + 1
            
        # Formatear para Tremor (Frontend)
        equipos_por_estado = [{"name": k, "value": v} for k, v in estados_count.items()]

        return {
            "total_equipos": total,
            "equipos_por_estado": equipos_por_estado,
            # ... mas métricas
        }