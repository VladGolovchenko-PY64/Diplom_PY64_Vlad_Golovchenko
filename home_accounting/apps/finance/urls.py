# apps/finance/urls.py
from django.urls import path
from .views import WalletView, TransactionListView, CategoryListView

urlpatterns = [
    path("wallet/", WalletView.as_view(), name="wallet"),
    path("transactions/", TransactionListView.as_view(), name="transactions"),
    path("categories/", CategoryListView.as_view(), name="categories"),
]
