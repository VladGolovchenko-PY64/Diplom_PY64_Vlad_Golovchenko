# apps/finance/urls.py
from django.urls import path
from .views import WalletListView, TransactionListView, CategoryListView

app_name = "finance"

urlpatterns = [
    path("wallets/", WalletListView.as_view(), name="wallets"),
    path("transactions/", TransactionListView.as_view(), name="transactions"),
    path("categories/", CategoryListView.as_view(), name="categories"),
]
