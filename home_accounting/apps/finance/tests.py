# apps/finance/tests.py
from django.test import TestCase
from apps.users.models import CustomUser
from .models import Wallet, Transaction, Category

class FinanceTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", password="12345")
        self.wallet = Wallet.objects.create(owner=self.user, balance=1000)

    def test_create_expense(self):
        category = Category.objects.create(owner=self.user, name="Продукты", type="expense")
        Transaction.objects.create(wallet=self.wallet, category=category, amount=100, date="2025-01-01", type="expense")
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 900.0)
