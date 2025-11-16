# apps/core/exceptions/db_exceptions.py
from .base_exceptions import AppBaseException


class DatabaseError(AppBaseException):
    status_code = 503
    message = "Ошибка соединения с базой данных. Повторите попытку позже."
