# apps/core/mixins.py
from django.db import models
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


class TimestampMixin(models.Model):
    """
    Добавляет created_at и updated_at к моделям.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserOwnedMixin(models.Model):
    """
    Для моделей, привязанных к пользователю.
    Используем строку settings.AUTH_USER_MODEL чтобы не импортировать модель напрямую.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_items"
    )

    class Meta:
        abstract = True


class ResponseMixin:
    """
    Примесь для унифицированных ответов DRF view'ов.
    """
    def success_response(self, data=None, message="OK", status_code=status.HTTP_200_OK):
        return Response({"message": message, "data": data}, status=status_code)

    def error_response(self, message="Ошибка", status_code=status.HTTP_400_BAD_REQUEST):
        return Response({"error": message}, status=status_code)
