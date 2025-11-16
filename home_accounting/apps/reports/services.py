# apps/reports/services.py
import os
from decimal import Decimal
import pandas as pd
from django.conf import settings
from django.db.models import Sum
from apps.finance.models import Transaction
from .models import Report

def generate_report(report: Report):
    """
    Генерация финансового отчёта в Excel и сохранение его файла в модели Report.
    """
    transactions = Transaction.objects.filter(
        wallet__owner=report.user,
        date__gte=report.start_date,
        date__lte=report.end_date,
    )

    # Считаем доходы и расходы
    income = transactions.filter(category__type="income").aggregate(total=Sum("amount"))["total"] or Decimal(0)
    expense = transactions.filter(category__type="expense").aggregate(total=Sum("amount"))["total"] or Decimal(0)

    data = []
    for t in transactions:
        data.append({
            "Дата": t.date,
            "Тип": "Доход" if t.category.type == "income" else "Расход",
            "Категория": t.category.name if t.category else "Без категории",
            "Сумма": t.amount,
            "Комментарий": t.comment or "",
        })

    df = pd.DataFrame(data)

    reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    file_name = f"report_{report.id}.xlsx"
    file_path = os.path.join(reports_dir, file_name)
    df.to_excel(file_path, index=False)

    report.file.name = f"reports/{file_name}"
    report.total_income = income
    report.total_expense = expense
    report.is_ready = True
    report.save()
