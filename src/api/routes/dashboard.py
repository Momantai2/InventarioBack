from fastapi import APIRouter, Depends
from src.application.services.Dashboard_service import DashboardService
from src.infrastructure.repositories.equipment_repository_impl import EquipmentRepositoryImpl
from src.infrastructure.repositories.historial_asignaciones_repository_impl import HistorialAsignacionesRepositoryImpl
from src.schemas.dashboard import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["Dashboard y Estadísticas"])

def get_dashboard_service():
    eq_repo = EquipmentRepositoryImpl()
    hist_repo = HistorialAsignacionesRepositoryImpl()
    return DashboardService(eq_repo, hist_repo)

@router.get("/overview", response_model=DashboardStats)
async def get_dashboard_overview(
    service: DashboardService = Depends(get_dashboard_service)
):
    """
    Consolida métricas de inventario para el dashboard principal.
    Incluye KPIs, distribución por categorías y feed de actividad.
    """
    return await service.get_overview_stats()