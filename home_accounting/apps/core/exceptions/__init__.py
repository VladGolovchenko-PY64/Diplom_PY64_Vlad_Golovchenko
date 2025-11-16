# apps/core/exceptions/__init__.py
# Экспорт основных исключений для удобства
from .base_exceptions import AppBaseException  # re-export для удобства
from .db_exceptions import DatabaseError
from .logic_exceptions import LogicError, UnauthorizedActionError, InsufficientFundsError
from .api_exceptions import APIError, PermissionDeniedError
