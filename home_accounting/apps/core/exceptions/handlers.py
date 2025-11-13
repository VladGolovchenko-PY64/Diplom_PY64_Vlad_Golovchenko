# apps/core/exceptions/handlers.py
from .base_exceptions import AppBaseException

def map_exception_to_response(exception):
    """
    Преобразует внутренние исключения в структуру JSON-ответа.
    """
    if isinstance(exception, AppBaseException):
        return {"status": exception.status_code, "message": exception.message}

    # Неизвестные ошибки
    return {"status": 500, "message": "Неизвестная ошибка сервера"}
