from django.urls import path
from .views_template import (
    AddWalletView, AddCategoryView,
    CategoryUpdateView, CategoryDeleteView,
    DashboardView, AddTransactionView
)

app_name = "finance"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("wallet/add/", AddWalletView.as_view(), name="add_wallet"),
    path("category/add/", AddCategoryView.as_view(), name="add_category"),
    path("category/edit/<int:pk>/", CategoryUpdateView.as_view(), name="category_edit"),
    path("category/delete/<int:pk>/", CategoryDeleteView.as_view(), name="category_delete"),
    path("transaction/add/", AddTransactionView.as_view(), name="add_transaction"),
]
