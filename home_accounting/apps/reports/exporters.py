import pandas as pd
from datetime import datetime
import os

def export_to_excel(transactions):
    """Генерация Excel файла из queryset Transaction"""
    data = []
    for t in transactions:
        data.append({
            "Дата": t.date,
            "Тип": t.type,
            "Сумма": t.amount,
            "Категория": t.category.name if t.category else "",
            "Комментарий": t.comment or ""
        })
    df = pd.DataFrame(data)
    filename = f"reports/report_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_excel(filename, index=False)
    return filename
