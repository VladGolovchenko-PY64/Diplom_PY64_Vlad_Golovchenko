# apps/users/errors.py
from apps.core.exceptions.logic_exceptions import LogicError

class UserAlreadyExistsError(LogicError):
    message = "Пользователь с таким email уже существует."
