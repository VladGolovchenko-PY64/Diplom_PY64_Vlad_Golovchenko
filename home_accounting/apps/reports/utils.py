# Можно добавить вспомогательные функции для фильтрации данных, агрегации, графиков и т.д.
from django.db.models import QuerySet

def filter_transactions(
    transactions: QuerySet,
    category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None
) -> QuerySet:

    if category:
        transactions = transactions.filter(category__name=category)
    if min_amount is not None:
        transactions = transactions.filter(amount__gte=min_amount)
    if max_amount is not None:
        transactions = transactions.filter(amount__lte=max_amount)
    return transactions
