# apps/reports/views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report
from .forms import ReportForm
from .tasks import generate_report_task
from django.db import transaction

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
        report.save()  # объект в БД создан, но транзакция ещё не зафиксирована

        # Запуск Celery только ПОСЛЕ commit транзакции
        transaction.on_commit(lambda: generate_report_task.delay(report.id))

        return super().form_valid(form)
