# apps/core/mixins.py
from django.db import models
from rest_framework.response import Response
from rest_framework import status

class ResponseMixin:
    """
    Примесь для унифицированных ответов API.
    """
    def success_response(self, data=None, message="OK", status_code=status.HTTP_200_OK):
        return Response({"message": message, "data": data}, status=status_code)

    def error_response(self, message="Ошибка", status_code=status.HTTP_400_BAD_REQUEST):
        return Response({"error": message}, status=status_code)


class TimestampMixin(models.Model):
    """
    Примесь для добавления полей created_at и updated_at к моделям.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserOwnedMixin(models.Model):
    """
    Примесь для моделей, которые привязаны к пользователю.
    """
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="%(class)s_items")

    class Meta:
        abstract = True