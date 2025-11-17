from django.db import models, transaction as db_transaction
from apps.core.mixins import TimestampMixin, UserOwnedMixin
from apps.users.models import CustomUser
from apps.core.exceptions.logic_exceptions import InsufficientFundsError

class Wallet(TimestampMixin, UserOwnedMixin):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="RUB")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="wallets")

    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency})"


class Category(TimestampMixin, UserOwnedMixin):
    INCOME = "income"
    EXPENSE = "expense"
    CATEGORY_TYPE_CHOICES = [(INCOME, "Доход"), (EXPENSE, "Расход")]

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)
    is_important = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(TimestampMixin, UserOwnedMixin):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="transactions")

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # новая транзакция
        old_amount = 0
        old_wallet = None
        old_category_type = None

        if not is_new:
            old = Transaction.objects.get(pk=self.pk)
            old_amount = old.amount
            old_wallet = old.wallet
            old_category_type = old.category.type if old.category else None

        with db_transaction.atomic():
            super().save(*args, **kwargs)

            # Если категория удалена — НЕ меняем баланс
            if self.category is None:
                pass
            else:
                if self.category.type == Category.INCOME:
                    self.wallet.balance += self.amount
                else:  # расход
                    if self.amount > self.wallet.balance:
                        raise InsufficientFundsError("Недостаточно средств на счете.")
                    self.wallet.balance -= self.amount

            self.wallet.save()

            # если редактирование и изменился кошелек или сумма
            if not is_new and old_wallet:
                new_category_type = self.category.type if self.category else None

                if old_wallet != self.wallet or old_amount != self.amount or old_category_type != new_category_type:

                    if old_category_type is not None:
                        if old_category_type == Category.INCOME:
                            old_wallet.balance -= old_amount
                        else:  # расход
                            old_wallet.balance += old_amount
                        old_wallet.save()

    def __str__(self):
        return f"{self.category} | {self.amount}"
