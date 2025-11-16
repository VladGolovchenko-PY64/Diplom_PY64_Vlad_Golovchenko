from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.mixins import TimestampMixin

class CustomUser(AbstractUser, TimestampMixin):
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = [
        (MALE, "Мужской"),
        (FEMALE, "Женский"),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.email})"

class Family(TimestampMixin):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(CustomUser, related_name="families")

    def __str__(self):
        return self.name
