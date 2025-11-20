# apps/reports/views.py
from django.db import transaction
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report
from .forms import ReportForm
from .tasks import generate_report_task
import logging

logger = logging.getLogger(__name__)

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = "reports/report_list.html"
    context_object_name = "reports"

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user).order_by("-created_at")

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    template_name = "reports/report_create.html"
    form_class = ReportForm
    success_url = reverse_lazy("reports:report_list")

    def form_valid(self, form):
        report = form.save(commit=False)
        report.user = self.request.user
        report.save()
        transaction.on_commit(lambda: generate_report_task.delay(report.id))
        return super().form_valid(form)


