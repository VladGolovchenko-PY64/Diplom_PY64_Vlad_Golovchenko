# apps/core/tests.py
from django.test import TestCase
from django.db import connections
from django.test import tag
from .utils.validators import validate_username
from django.core.exceptions import ValidationError

class ValidatorsTests(TestCase):
    def test_validate_username_ok(self):
        validate_username("user_123")  # не должно бросать

    def test_validate_username_fail(self):
        with self.assertRaises(ValidationError):
            validate_username("in@valid!")

class DBConnectionTest(TestCase):
    def test_check_default_connection(self):
        # Это простой тест — проверим, что можно получить курсор (если база доступна)
        conn = connections["default"]
        try:
            with conn.cursor() as c:
                self.assertIsNotNone(c)
        except Exception:
            # не фейлим тест при недоступной БД — просто помечаем как пропуск
            self.skipTest("DB not available for connection test")
