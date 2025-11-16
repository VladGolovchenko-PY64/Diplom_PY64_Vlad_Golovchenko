# apps/core/exceptions/handlers.py
from .api_exceptions import APIError
from .db_exceptions import DatabaseError

def map_exception_to_response(exc):
    """
    Преобразует исключение в словарь с полями 'message' и 'status'.
    """
    if isinstance(exc, APIError):
        return {"message": str(exc), "status": exc.status_code}
    elif isinstance(exc, DatabaseError):
        return {"message": "Ошибка базы данных", "status": 500}
    else:
        return {"message": "Внутренняя ошибка сервера", "status": 500}
