# apps/core/exceptions/logic_exceptions.py
from .base_exceptions import AppBaseException


class LogicError(AppBaseException):
    status_code = 400
    message = "Ошибка логики приложения."


class UnauthorizedActionError(AppBaseException):
    status_code = 403
    message = "Действие не разрешено для текущего пользователя."


class InsufficientFundsError(AppBaseException):
    status_code = 400
    message = "Недостаточно средств на счёте."
