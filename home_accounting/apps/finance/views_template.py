from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.db.models import Sum
from .forms import WalletForm, CategoryForm, TransactionForm
from .models import Wallet, Category, Transaction

class AddWalletView(View):
    template_name = "finance/add_wallet.html"

    def get(self, request):
        form = WalletForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user   # <- исправлено
            wallet.save()
            return redirect("finance:dashboard")
        return render(request, self.template_name, {"form": form})

class AddCategoryView(View):
    template_name = "finance/add_category.html"

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # <- исправлено
            category.save()
            return redirect("finance:dashboard")
        return render(request, self.template_name, {"form": form})

class AddTransactionView(View):
    template_name = "finance/add_transaction.html"

    def get(self, request):
        form = TransactionForm(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # назначаем владельца

            # Обновляем баланс кошелька в зависимости от типа категории
            wallet = transaction.wallet
            if transaction.category.type == Category.EXPENSE:
                if wallet.balance < transaction.amount:
                    form.add_error("amount", "Недостаточно средств на кошельке.")
                    return render(request, self.template_name, {"form": form})
                wallet.balance -= transaction.amount
            else:  # доход
                wallet.balance += transaction.amount

            wallet.save()
            transaction.save()
            return redirect("finance:dashboard")

        return render(request, self.template_name, {"form": form})

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "finance/edit_category.html"
    success_url = reverse_lazy("finance:dashboard")

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "finance/delete_category.html"
    success_url = reverse_lazy("finance:dashboard")

class DashboardView(TemplateView):
    template_name = "finance/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Получаем кошельки и транзакции пользователя
        wallets = Wallet.objects.filter(user=user)
        transactions = Transaction.objects.filter(user=user).order_by('date', 'id')  # по дате и id

        context["wallets"] = Wallet.objects.filter(user=user)
        context["categories"] = Category.objects.filter(user=user)
        context["transactions"] = transactions

        # Рассчитываем суммарные расходы по категориям
        category_sums = {}
        for category in context["categories"]:
            total = transactions.filter(
                category=category, category__type=Category.EXPENSE
            ).aggregate(total=Sum('amount'))['total'] or 0
            category_sums[category.name] = total
        context["category_sums"] = category_sums

        # Вычисляем баланс кошелька после каждой транзакции
        # Словарь для хранения текущего баланса каждого кошелька
        wallet_current_balance = {w.id: w.balance for w in wallets}
        # Список балансов для каждой транзакции (отображение в таблице)
        transaction_balances = []

        for tx in transactions:
            if tx.category.type == Category.EXPENSE:
                wallet_current_balance[tx.wallet.id] -= tx.amount
            else:  # доход
                wallet_current_balance[tx.wallet.id] += tx.amount
            transaction_balances.append(wallet_current_balance[tx.wallet.id])

        context["transaction_balances"] = transaction_balances

        # После расчёта transaction_balances
        transactions_with_balance = list(zip(transactions, transaction_balances))
        context["transactions_with_balance"] = transactions_with_balance


        # Передаем актуальные балансы кошельков для верхней части страницы
        wallet_balances = {w.id: w.balance for w in wallets}
        context["wallet_balances"] = wallet_balances

        return context





