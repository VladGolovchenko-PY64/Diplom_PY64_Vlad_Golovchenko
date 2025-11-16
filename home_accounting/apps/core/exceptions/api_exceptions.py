# apps/core/exceptions/api_exceptions.py
from .base_exceptions import AppBaseException


class APIError(AppBaseException):
    status_code = 500
    message = "Ошибка при обработке API-запроса."


class PermissionDeniedError(AppBaseException):
    status_code = 403
    message = "Недостаточно прав для выполнения действия."
