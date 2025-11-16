# apps/finance/tests.py
from django.test import TestCase
from apps.users.models import CustomUser
from .models import Wallet, Category, Transaction
from .errors import InsufficientFundsError
from datetime import date

class FinanceTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", password="12345")
        self.wallet = Wallet.objects.create(user=self.user, name="Основной", balance=1000)
        self.income_cat = Category.objects.create(owner=self.user, name="Зарплата", type="income")
        self.expense_cat = Category.objects.create(owner=self.user, name="Еда", type="expense")

    def test_deposit_withdraw(self):
        self.wallet.deposit(500)
        self.assertEqual(self.wallet.balance, 1500)
        self.wallet.withdraw(400)
        self.assertEqual(self.wallet.balance, 1100)
        with self.assertRaises(InsufficientFundsError):
            self.wallet.withdraw(2000)

    def test_transaction_creation(self):
        t1 = Transaction.objects.create(wallet=self.wallet, category=self.income_cat, amount=500, date=date.today())
        t2 = Transaction.objects.create(wallet=self.wallet, category=self.expense_cat, amount=300, date=date.today())
        self.assertEqual(t1.amount, 500)
        self.assertEqual(t2.amount, 300)
