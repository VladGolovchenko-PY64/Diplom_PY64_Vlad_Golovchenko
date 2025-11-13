# apps/users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import CustomUser, Family

@receiver(post_save, sender=CustomUser)
def create_default_family(sender, instance, created, **kwargs):
    """
    Создаем семью автоматически для новых пользователей, если необходимо.
    """
    if created:
        # Пример: можно создавать отдельную семью для первого пользователя
        # Или оставлять пустым и создавать через логику сервиса
        pass
