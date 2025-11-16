from django import forms
from .models import Wallet, Category, Transaction

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'balance', 'currency']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'is_important']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["wallet", "category", "amount", "description", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),  # календарик
            "description": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        # Ограничиваем кошельки и категории только текущим пользователем
        self.fields["wallet"].queryset = Wallet.objects.filter(user=user)
        self.fields["category"].queryset = Category.objects.filter(user=user)
