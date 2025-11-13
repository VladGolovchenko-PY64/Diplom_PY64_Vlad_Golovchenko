# apps/finance/errors.py
from apps.core.exceptions.logic_exceptions import LogicError

class InsufficientFundsError(LogicError):
    message = "Недостаточно средств на счёте!"
