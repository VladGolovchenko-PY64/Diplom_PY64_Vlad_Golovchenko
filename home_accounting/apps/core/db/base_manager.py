# apps/core/db/base_manager.py
from django.db import models

class BaseManager(models.Manager):
    """
    Базовый менеджер с дополнительными методами для всех моделей.
    """
    def active(self):
        return self.filter(is_active=True)
