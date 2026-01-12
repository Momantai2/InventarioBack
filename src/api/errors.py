from fastapi import Request, status
from fastapi.responses import JSONResponse
import structlog
import os
logger = structlog.get_logger()

async def global_exception_handler(request: Request, exc: Exception):
    logger.error("request_failed", path=request.url.path, error=str(exc))
    
    # Podrías personalizar errores según el tipo (ej. errores de Supabase)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal Server Error",
            "detail": str(exc) if os.getenv("DEBUG") else "Consulte con el administrador"
        }
    )