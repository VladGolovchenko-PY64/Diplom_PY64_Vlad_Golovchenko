# config/exceptions_handler.py
from django.http import JsonResponse
from apps.core.exceptions.handlers import map_exception_to_response
import traceback
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def handle_exception(exc):
    """
    Универсальный, безопасный обработчик исключений.
    - контролируемые исключения → отдаём их сообщение
    - остальные → логируем и отдаём безопасное сообщение
    """
    try:
        response = map_exception_to_response(exc)
        status = response.get("status", 500)
        message = response.get("message", "Внутренняя ошибка сервера")

        # Логируем для разработчиков
        logger.exception(f"Handled exception: {exc}")

        if settings.DEBUG:
            return JsonResponse({
                "detail": message,
                "exception": str(exc),
                "traceback": traceback.format_exc(),
            }, status=status)

        # В продакшене — никаких деталей!
        return JsonResponse({
            "detail": message
        }, status=status)

    except Exception as e:
        logger.error(
            "Exception in exception handler: %s\n%s",
            e,
            traceback.format_exc()
        )

        if settings.DEBUG:
            # В DEBUG можно показать
            return JsonResponse({
                "detail": "Ошибка в обработчике исключений",
                "exception": str(e),
                "traceback": traceback.format_exc()
            }, status=500)

        # В продакшене — строго минимальный ответ
        return JsonResponse({
            "detail": "Внутренняя ошибка сервера"
        }, status=500)
