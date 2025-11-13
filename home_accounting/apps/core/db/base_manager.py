# apps/core/db/base_manager.py
from django.db import models
from apps.core.exceptions.db_exceptions import DatabaseError


class BaseManager(models.Manager):
    """
    Кастомный менеджер, перехватывающий ошибки БД.
    """

    def safe_get(self, **kwargs):
        """
        Получает объект из базы данных по условиям kwargs.
        Если объект не найден, возвращает None.
        При возникновении других исключений, поднимает DatabaseError.
        """
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        except Exception as exc:
            raise DatabaseError(f"Ошибка при запросе данных: {exc}")

    def safe_filter(self, **kwargs):
        """
        Фильтрует объекты из базы данных по условиям kwargs.
        При возникновении исключений, поднимает DatabaseError.
        """
        try:
            return self.filter(**kwargs)
        except Exception as exc:
            raise DatabaseError(f"Ошибка при фильтрации данных: {exc}")
