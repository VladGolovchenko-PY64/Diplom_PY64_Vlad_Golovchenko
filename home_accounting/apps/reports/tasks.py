# apps/reports/tasks.py
from celery import shared_task
from .models import Report
from .services import generate_report

@shared_task
def generate_report_task(report_id):
    report = Report.objects.get(id=report_id)
    generate_report(report)
