# apps/finance/models.py
from django.db import models, transaction
from apps.core.mixins import TimestampMixin, UserOwnedMixin
from apps.users.models import CustomUser
from apps.core.exceptions.logic_exceptions import InsufficientFundsError


class Wallet(TimestampMixin):
    """
    Счет/Кошелек пользователя или семейный.
    """
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="wallets",
        verbose_name="Владелец"
    )
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="RUB")

    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency})"

    @transaction.atomic
    def deposit(self, amount):
        """Безопасное пополнение кошелька"""
        self.balance += amount
        self.save(update_fields=["balance"])

    @transaction.atomic
    def withdraw(self, amount):
        """Безопасное снятие средств"""
        if amount > self.balance:
            raise InsufficientFundsError("Недостаточно средств на счете.")
        self.balance -= amount
        self.save(update_fields=["balance"])


class Category(TimestampMixin, UserOwnedMixin):
    """
    Категории расходов/доходов.
    """
    INCOME = 'income'
    EXPENSE = 'expense'
    CATEGORY_TYPE_CHOICES = [
        (INCOME, 'Доход'),
        (EXPENSE, 'Расход'),
    ]

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(TimestampMixin, UserOwnedMixin):
    """
    Транзакции (расходы/доходы).
    """
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField()

    def save(self, *args, **kwargs):
        """
        Проверка баланса при расходе. Если тип категории — expense,
        уменьшаем баланс; если income — увеличиваем.
        """
        if self.category and self.category.type == Category.EXPENSE:
            if self.amount > self.wallet.balance:
                raise InsufficientFundsError("Недостаточно средств на счете.")
            self.wallet.withdraw(self.amount)
        elif self.category and self.category.type == Category.INCOME:
            self.wallet.deposit(self.amount)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} | {self.amount}"
