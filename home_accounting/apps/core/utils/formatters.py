# apps/core/utils/formatters.py
from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Форматирует дату/время в ISO-представлении"""
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""
