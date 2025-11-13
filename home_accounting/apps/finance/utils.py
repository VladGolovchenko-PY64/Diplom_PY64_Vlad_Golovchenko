# apps/finance/utils.py
from datetime import date

def get_current_month_transactions(transactions):
    """
    Фильтрует транзакции текущего месяца.
    """
    today = date.today()
    return transactions.filter(date__month=today.month, date__year=today.year)
