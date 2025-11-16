# apps/reports/utils.py
def filter_transactions(transactions, category=None, min_amount=None, max_amount=None):
    if category:
        transactions = transactions.filter(category__name=category)
    if min_amount:
        transactions = transactions.filter(amount__gte=min_amount)
    if max_amount:
        transactions = transactions.filter(amount__lte=max_amount)
    return transactions
