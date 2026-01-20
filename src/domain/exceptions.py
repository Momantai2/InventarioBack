class DomainError(Exception):
    """Clase base para errores de dominio"""
    pass

class EntityAlreadyExistsError(DomainError):
    """Cuando un registro ya existe (ej: Serie duplicada)"""
    pass

class EntityNotFoundError(DomainError):
    """Cuando un registro no existe"""
    pass

class BusinessRuleError(DomainError):
    """Cuando se rompe una regla de negocio"""
    pass

# AÑADE ESTA CLASE:
class BadRequestError(DomainError):
    """Cuando los datos enviados son incorrectos o la petición es inválida"""
    pass