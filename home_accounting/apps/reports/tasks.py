# apps/reports/tasks.py
import logging
from celery import shared_task
from .models import Report
from .services import generate_report

logger = logging.getLogger(__name__)

@shared_task
def generate_report_task(report_id):
    try:
        report = Report.objects.get(id=report_id)
        logger.info(f"Starting report generation: {report}")
        generate_report(report)
        logger.info(f"Report generated successfully: {report}")
    except Report.DoesNotExist:
        logger.error(f"Report with id {report_id} does not exist.")
    except Exception as e:
        logger.exception(f"Error generating report {report_id}: {e}")
