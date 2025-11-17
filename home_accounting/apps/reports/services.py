# apps/reports/services.py
import os
from decimal import Decimal
import pandas as pd
from django.conf import settings
from django.db.models import Sum
from apps.finance.models import Transaction, Category
from .models import Report

def generate_report(report: Report):
    """
    Генерация финансового отчёта в Excel и сохранение его файла в модели Report.
    Работает асинхронно через Celery.
    """

    # Получаем все транзакции пользователя за период
    transactions = Transaction.objects.filter(
        user=report.user,
        date__gte=report.start_date,
        date__lte=report.end_date,
    ).select_related('category')

    # Считаем общие доходы и расходы
    income = transactions.filter(category__type=Category.INCOME).aggregate(total=Sum("amount"))["total"] or Decimal(0)
    expense = transactions.filter(category__type=Category.EXPENSE).aggregate(total=Sum("amount"))["total"] or Decimal(0)

    data = []
    for t in transactions:
        category_type = t.category.type if t.category else None
        data.append({
            "Дата": t.date,
            "Тип": "Доход" if category_type == Category.INCOME else "Расход",
            "Категория": t.category.name if t.category else "Без категории",
            "Сумма": t.amount,
            "Комментарий": t.description or "",
        })

    # Создаём DataFrame
    df = pd.DataFrame(data)

    # Папка для сохранения отчётов
    reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    file_name = f"report_{report.id}.xlsx"
    file_path = os.path.join(reports_dir, file_name)

    # Сохраняем Excel
    df.to_excel(file_path, index=False)

    # Обновляем модель Report
    report.file.name = f"reports/{file_name}"
    report.total_income = income
    report.total_expense = expense
    report.is_ready = True
    report.save()
