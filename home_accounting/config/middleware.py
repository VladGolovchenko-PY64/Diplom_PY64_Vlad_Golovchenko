# config/middleware.py
from django.utils.deprecation import MiddlewareMixin
from config.exceptions_handler import handle_exception

class ExceptionMiddleware(MiddlewareMixin):
    """
    Глобальная обработка исключений: перехватывает исключения и
    возвращает JSON-ответ через exceptions_handler (для API).
    """
    def process_exception(self, request, exception):
        # handle_exception возвращает HttpResponse/JsonResponse
        return handle_exception(exception)
