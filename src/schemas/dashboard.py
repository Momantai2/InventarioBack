from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DashboardKPIs(BaseModel):
    total: int
    disponibles: int
    asignados: int
    mantenimiento: int
    baja: int

    disponibilidad_pct: float

class DashboardCharts(BaseModel):
    estados: List[Dict[str, Any]]
    categorias: List[Dict[str, Any]]
    proveedores: List[Dict[str, Any]]    
    sedes: List[Dict[str, Any]]


class DashboardStats(BaseModel):
    kpis: DashboardKPIs
    charts: DashboardCharts
    ultimos_movimientos: List[Dict[str, Any]]