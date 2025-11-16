# config/exceptions_handler.py
from django.http import JsonResponse
from apps.core.exceptions.handlers import map_exception_to_response
import traceback
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def handle_exception(exc):
    """
    Универсальный обработчик исключений.
    Для известных App-исключений возвращает контролируемое сообщение.
    Для прочих — логирует и возвращает generic ответ.
    """
    try:
        response = map_exception_to_response(exc)
        status = response.get("status", 500)
        message = response.get("message", "Внутренняя ошибка сервера")

        # Логируем подробности для разработчиков
        logger.exception(f"Handled exception: {exc}")

        # В DEBUG включаем подробный traceback в JSON
        if settings.DEBUG:
            return JsonResponse({
                "detail": message,
                "exception": str(exc),
                "traceback": traceback.format_exc()
            }, status=status)

        return JsonResponse({"detail": message}, status=status)

    except Exception as e:
        # Если что-то сломалось в обработчике, вернём минимальный ответ
        logger.error("Exception in exception handler: %s\n%s", e, traceback.format_exc())
        return JsonResponse({
            "detail": "Внутренняя ошибка сервера",
            "exception": str(e),
            "traceback": traceback.format_exc() if settings.DEBUG else ""
        }, status=500)
