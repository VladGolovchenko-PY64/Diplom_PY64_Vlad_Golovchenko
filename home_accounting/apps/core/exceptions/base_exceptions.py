# apps/core/exceptions/base_exceptions.py

class AppBaseException(Exception):
    """Базовое приложение исключений"""
    status_code = 500
    message = "Внутренняя ошибка приложения"

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)
