# apps/finance/services.py
from decimal import Decimal
from .models import Transaction, Wallet
from .errors import InsufficientFundsError

def create_transaction(wallet, data):
    """
    Создание транзакции (доход или расход).
    Проверка баланса.
    """
    amount = Decimal(data["amount"])
    if data["type"] == "expense" and wallet.balance < amount:
        raise InsufficientFundsError("Недостаточно средств на счёте!")

    if data["type"] == "income":
        wallet.balance += amount
    else:
        wallet.balance -= amount
    wallet.save()

    Transaction.objects.create(wallet=wallet, **data)


def get_balance(user):
    wallet, _ = Wallet.objects.get_or_create(owner=user)
    return wallet.balance
