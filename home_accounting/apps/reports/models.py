# apps/reports/models.py
from django.db import models
from django.conf import settings
from apps.core.mixins import TimestampMixin

User = settings.AUTH_USER_MODEL

class Report(TimestampMixin):
    """
    Финансовый отчёт пользователя (период, категории, итоги)
    """
    PERIOD_CHOICES = (
        ("month", "Месячный"),
        ("year", "Годовой"),
        ("custom", "Произвольный"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    file = models.FileField(upload_to="reports/", null=True, blank=True)
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expense = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_ready = models.BooleanField(default=False)

    def __str__(self):
        return f"Отчёт {self.user.username} ({self.period_type})"
