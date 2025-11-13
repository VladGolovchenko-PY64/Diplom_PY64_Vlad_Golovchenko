# apps/reports/views.py
from django.db.models import QuerySet
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from .services import generate_report
from apps.core.mixins import ResponseMixin
from .tasks import generate_report_task

class ReportListView(ResponseMixin, generics.ListCreateAPIView):
    """
    Список и создание отчётов пользователя
    """
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> "QuerySet[Report]":
        return Report.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        report = serializer.save(user=self.request.user)
        generate_report_task.delay(report.id)  # асинхронно
        return report
