from typing import Dict, Any

class DashboardService:
    def __init__(self, equipment_repo, history_repo):
        self.eq_repo = equipment_repo
        self.hist_repo = history_repo

    async def get_overview_stats(self) -> Dict[str, Any]:
        # 1. Obtener datos
        equipos = self.eq_repo.get_all()
        historial = self.hist_repo.get_all_historial()
        
        # 2. Inicializar contadores
        total_equipos = len(equipos)
        por_estado = {}
        por_categoria = {}
        por_sede = {}
        por_proveedor = {"Propio": 0, "Renting": 0}
        
        # 3. Procesar Equipos en una sola pasada
        for eq in equipos:
            # --- Conteo por Estado ---
            estado = eq.get("estados", {}).get("nombre", "OTRO").upper().strip()
            por_estado[estado] = por_estado.get(estado, 0) + 1
            
            # --- Conteo por Categoría ---
            cat = eq.get("modelos", {}).get("tipos_equipo", {}).get("nombre", "SIN CATEGORÍA").upper()
            por_categoria[cat] = por_categoria.get(cat, 0) + 1
            
            # --- Conteo por Proveedor ---
            if eq.get("proveedores_renting"):
                por_proveedor["Renting"] += 1
            else:
                por_proveedor["Propio"] += 1
            
            # --- Conteo por Sede (Identación Corregida) ---
            ubicacion = eq.get("ubicaciones_detalladas")
            if ubicacion:
                sede_obj = ubicacion.get("sedes_agencias")
                if sede_obj:
                    nombre_sede = sede_obj.get("nombre", "OFICINA CENTRAL")
                else:
                    nombre_sede = "UBICACIÓN SIN SEDE"
            else:
                nombre_sede = "ALMACÉN TI"

            # El conteo debe estar dentro del bucle for
            sede_key = nombre_sede.upper().strip()
            por_sede[sede_key] = por_sede.get(sede_key, 0) + 1

        # 4. Formatear respuesta final
        disponibles = por_estado.get("DISPONIBLE", 0)
        asignados = por_estado.get("ASIGNADO", 0)
        mantenimiento = por_estado.get("MANTENIMIENTO", 0)
        baja = por_estado.get("INOPERATIVA", 0) 

        return {
            "kpis": {
                "total": total_equipos,
                "disponibles": disponibles,
                "asignados": asignados,
                "mantenimiento": mantenimiento,
                "baja": baja,
                "disponibilidad_pct": round((disponibles / total_equipos * 100), 2) if total_equipos > 0 else 0
            },
            "charts": {
                "estados": [{"name": k, "value": v} for k, v in por_estado.items()],
                "categorias": [{"name": k, "value": v} for k, v in por_categoria.items()],
                "proveedores": [{"name": k, "value": v} for k, v in por_proveedor.items()],
                "sedes": [{"name": k, "value": v} for k, v in por_sede.items()]
            },
            "ultimos_movimientos": historial[:6]
        }