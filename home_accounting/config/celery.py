# config/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("home_accounting")
# Загружаем конфигурацию Celery из переменных Django settings, префикс CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")
# Автоматическое обнаружение задач в приложениях
app.autodiscover_tasks()
