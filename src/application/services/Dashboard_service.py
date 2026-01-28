from typing import Dict, Any

class DashboardService:
    def __init__(self, equipment_repo, history_repo):
        self.eq_repo = equipment_repo
        self.hist_repo = history_repo

    async def get_overview_stats(self) -> Dict[str, Any]:
        # 1. Obtener datos (OJO: get_all_paginated devuelve un dict con 'items')
        res_equipos = self.eq_repo.get_all_paginated(page=1, page_size=1000)
        equipos = res_equipos.get("items", []) # Extraemos la lista real
        
        historial = self.hist_repo.get_all_historial()
        
        # 2. Inicializar contadores
        total_equipos = len(equipos)
        por_estado = {}
        por_categoria = {}
        por_sede = {}
        por_proveedor = {"Propio": 0, "Renting": 0}
        
        # 3. Procesar Equipos
        for eq in equipos:
            # --- Conteo por Estado ---
            # Corregido: Usar .get() que es el método de diccionarios en Python
            estado_obj = eq.get("estados")
            nombre_estado = "OTRO"
            if isinstance(estado_obj, dict):
                nombre_estado = estado_obj.get("nombre", "OTRO")
            
            estado_key = nombre_estado.upper().strip()
            por_estado[estado_key] = por_estado.get(estado_key, 0) + 1
            
            # --- Conteo por Categoría ---
            modelo_obj = eq.get("modelos")
            cat_nombre = "SIN CATEGORÍA"
            if isinstance(modelo_obj, dict):
                tipo = modelo_obj.get("tipos_equipo")
                if isinstance(tipo, dict):
                    cat_nombre = tipo.get("nombre", "SIN CATEGORÍA")
            
            cat_key = cat_nombre.upper().strip()
            por_categoria[cat_key] = por_categoria.get(cat_key, 0) + 1
            
            # --- Conteo por Proveedor ---
            if eq.get("proveedores_renting"):
                por_proveedor["Renting"] += 1
            else:
                por_proveedor["Propio"] += 1
            
            # --- Conteo por Sede ---
            ubicacion = eq.get("ubicaciones_detalladas")
            nombre_sede = "ALMACÉN TI"
            if isinstance(ubicacion, dict):
                sede_obj = ubicacion.get("sedes_agencias")
                if isinstance(sede_obj, dict):
                    nombre_sede = sede_obj.get("nombre", "OFICINA CENTRAL")
            
            sede_key = nombre_sede.upper().strip()
            por_sede[sede_key] = por_sede.get(sede_key, 0) + 1

        # 4. Formatear respuesta final
        return {
            "kpis": {
                "total": total_equipos,
                "disponibles": por_estado.get("DISPONIBLE", 0),
                "asignados": por_estado.get("ASIGNADO", 0),
                "mantenimiento": por_estado.get("MANTENIMIENTO", 0),
                "baja": por_estado.get("INOPERATIVA", 0),
                "disponibilidad_pct": round((por_estado.get("DISPONIBLE", 0) / total_equipos * 100), 2) if total_equipos > 0 else 0
            },
            "charts": {
                "estados": [{"name": k, "value": v} for k, v in por_estado.items()],
                "categorias": [{"name": k, "value": v} for k, v in por_categoria.items()],
                "proveedores": [{"name": k, "value": v} for k, v in por_proveedor.items()],
                "sedes": [{"name": k, "value": v} for k, v in por_sede.items()]
            },
            "ultimos_movimientos": historial[:6] if historial else []
        }