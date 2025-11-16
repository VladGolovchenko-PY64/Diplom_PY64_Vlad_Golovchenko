# apps/reports/tests.py
from django.test import TestCase
from apps.users.models import CustomUser
from apps.finance.models import Wallet, Transaction, Category
from .models import Report
from datetime import date

class ReportTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", password="12345")
        self.wallet = Wallet.objects.create(owner=self.user, balance=1000)
        self.category = Category.objects.create(owner=self.user, name="Еда", type="expense")
        Transaction.objects.create(wallet=self.wallet, category=self.category, amount=200, date=date.today(), type="expense")

    def test_report_creation(self):
        report = Report.objects.create(
            user=self.user,
            period_type="month",
            start_date=date(2025, 11, 1),
            end_date=date(2025, 11, 30)
        )
        self.assertEqual(report.total_income, 0)
        self.assertEqual(report.total_expense, 0)
