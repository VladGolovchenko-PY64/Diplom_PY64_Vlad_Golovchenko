# apps/finance/services.py
from .models import Wallet, Transaction, Category
from apps.core.exceptions.logic_exceptions import LogicError
from django.db import transaction as db_transaction

def create_wallet(user, name, initial_balance=0):
    wallet = Wallet.objects.create(user=user, name=name, balance=initial_balance)
    return wallet

def add_transaction(wallet, category, amount, comment="", date=None):
    with db_transaction.atomic():
        if category.type == Category.EXPENSE and amount > wallet.balance:
            raise LogicError("Недостаточно средств на счете.")
        transaction = Transaction.objects.create(
            wallet=wallet, category=category, amount=amount, comment=comment, date=date
        )
        if category.type == Category.INCOME:
            wallet.deposit(amount)
        else:
            wallet.withdraw(amount)
    return transaction
