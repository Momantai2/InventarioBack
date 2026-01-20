import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Importación de Rutas
from src.api.routes.inventory import router as equipment_router
from src.api.routes.persons import router as person_router
from src.api.routes.catalog import router as catalog_router
from src.api.routes.organizacion import router as org_router
from src.api.routes.insumos import router as insumos_router, router1 as movimientos_router
from src.api.routes.asignaciones import router as asignaciones_router
from src.api.routes.matenimiento import router as mantenimientos_router, router1 as movimientos_mantenimiento
from src.api.routes.dashboard import router as dashboard_router
# Importación de Manejo de Errores
from src.domain.exceptions import DomainError
from src.api.errors import domain_exception_handler, global_exception_handler

load_dotenv()

app = FastAPI(
    title="Inventory API",
    description="Sistema de gestión de activos",
    version="1.0"
)

# --- CONFIGURACIÓN DE ERRORES ---
# Captura errores específicos de lógica de negocio (400, 404, 409, 422)
app.add_exception_handler(DomainError, domain_exception_handler)
# Captura errores inesperados del sistema (500)
app.add_exception_handler(Exception, global_exception_handler)

# --- MIDDLEWARES ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTRO DE RUTAS (VERSIONADO) ---
# Usar /api/v1 es una práctica Senior para permitir cambios futuros sin romper el Front
api_prefix = "/api"

app.include_router(equipment_router, prefix=api_prefix, tags=["Equipos"])
app.include_router(person_router, prefix=api_prefix, tags=["Personas"])
app.include_router(catalog_router, prefix=api_prefix, tags=["Catálogos"])
app.include_router(org_router, prefix=api_prefix, tags=["Organización"])
app.include_router(insumos_router, prefix=api_prefix)
app.include_router(movimientos_router, prefix=api_prefix)
app.include_router(asignaciones_router, prefix=api_prefix)
app.include_router(mantenimientos_router, prefix=api_prefix)
app.include_router(movimientos_mantenimiento, prefix=api_prefix)
app.include_router(dashboard_router, prefix=api_prefix)

@app.get("/", tags=["Health"])
def read_root():
    return {
        "status": "online",
        "message": "Inventory API Running",
        "version": "1.1.0"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # El reload solo se activa en desarrollo
    is_dev = os.getenv("ENVIRONMENT") == "development"
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=is_dev)