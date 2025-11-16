# apps/reports/views.py
from rest_framework import generics, permissions
from apps.core.mixins import ResponseMixin
from .models import Report
from .serializers import ReportSerializer
from .services import generate_report

class ReportListView(ResponseMixin, generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        report = serializer.save(user=self.request.user)
        generate_report(report)
        return report
