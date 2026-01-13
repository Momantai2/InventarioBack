from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.domain.exceptions import DomainError, EntityNotFoundError, EntityAlreadyExistsError, BusinessRuleError
import os

# 1. Manejador para errores de lógica de negocio (Dominio)
async def domain_exception_handler(request: Request, exc: DomainError):
    status_code = status.HTTP_400_BAD_REQUEST
    
    if isinstance(exc, EntityNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, EntityAlreadyExistsError):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(exc, BusinessRuleError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": exc.__class__.__name__,
            "message": str(exc)
        }
    )

# 2. Manejador para errores inesperados del servidor (Global)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "InternalServerError",
            "message": "Ocurrió un error inesperado en el servidor.",
            "detail": str(exc) if os.getenv("ENVIRONMENT") == "development" else None
        }
    )