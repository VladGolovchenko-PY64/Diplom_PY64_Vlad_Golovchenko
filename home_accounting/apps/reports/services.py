# apps/reports/services.py
import os
from decimal import Decimal
import pandas as pd  # для работы с DataFrame и Excel
from django.conf import settings
from django.db.models import Sum
from apps.finance.models import Transaction
from .models import Report

def generate_report(report: Report):
    """
    Генерация финансового отчёта в Excel и сохранение его файла в модели Report.
    """
    # Получаем все транзакции пользователя за период отчёта
    transactions = Transaction.objects.filter(
        wallet__owner=report.user,
        date__gte=report.start_date,
        date__lte=report.end_date,
    )

    # Считаем доходы и расходы
    income = transactions.filter(type="income").aggregate(total=Sum("amount"))["total"] or Decimal(0)
    expense = transactions.filter(type="expense").aggregate(total=Sum("amount"))["total"] or Decimal(0)

    # Создаём DataFrame для Excel
    data = []
    for t in transactions:
        data.append({
            "Дата": t.date,
            "Тип": "Доход" if t.type == "income" else "Расход",
            "Категория": t.category.name if t.category else "Без категории",
            "Сумма": t.amount,
            "Комментарий": t.comment or "",
        })

    df = pd.DataFrame(data)

    # Папка для отчётов
    reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Сохраняем Excel
    file_name = f"report_{report.id}.xlsx"
    file_path = os.path.join(reports_dir, file_name)
    df.to_excel(file_path, index=False)

    # Сохраняем информацию в модели
    report.file.name = f"reports/{file_name}"
    report.total_income = income
    report.total_expense = expense
    report.is_ready = True
    report.save()
