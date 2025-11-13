# apps/reports/tasks.py
from django.core.exceptions import ObjectDoesNotExist
import logging
from celery import shared_task
from .models import Report
from .services import generate_report

logger = logging.getLogger(__name__)

@shared_task
def generate_report_task(report_id):
    try:
        report = Report.objects.get(id=report_id)
    except ObjectDoesNotExist:
        logger.error(f"Report with id={report_id} does not exist.")
        return
    generate_report(report)
