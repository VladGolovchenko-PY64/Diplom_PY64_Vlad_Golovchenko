# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.mixins import TimestampMixin

class CustomUser(AbstractUser, TimestampMixin):
    """
    Модель пользователя.
    """
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский')
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_admin_user = models.BooleanField(default=False)  # родитель
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.email})"


class Family(TimestampMixin):
    """
    Семейная группа.
    """
    name = models.CharField(max_length=50)
    members = models.ManyToManyField("users.CustomUser", related_name="families")
    owner = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="owned_families")

    def __str__(self):
        return self.name
