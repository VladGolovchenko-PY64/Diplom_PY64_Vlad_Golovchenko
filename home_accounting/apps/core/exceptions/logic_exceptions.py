# apps/core/exceptions/logic_exceptions.py
from .base_exceptions import AppBaseException


class LogicError(AppBaseException):
    """Ошибка логики приложения."""
    status_code = 400

    def __init__(self, message=None):
        self.message = message or "Ошибка логики приложения."
        super().__init__(self.message)


class UnauthorizedActionError(AppBaseException):
    """Ошибка при попытке действия, не разрешённого пользователю."""

    def __init__(self, message=None):
        self.message = message or "Это действие не разрешено для текущего пользователя."
        super().__init__(self.message)


class InsufficientFundsError(AppBaseException):
    """Ошибка при недостатке средств на счёте."""

    def __init__(self, message=None):
        self.message = message or "Недостаточно средств на счёте для выполнения этого действия."
        super().__init__(self.message)
