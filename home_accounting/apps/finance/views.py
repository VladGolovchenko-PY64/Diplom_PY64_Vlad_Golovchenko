# apps/finance/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Wallet, Transaction, Category
from .serializers import WalletSerializer, TransactionSerializer, CategorySerializer
from .services import create_transaction, get_balance
from apps.core.mixins import ResponseMixin


class WalletView(ResponseMixin, generics.RetrieveAPIView):
    """
    Баланс текущего пользователя.
    """
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        wallet, _ = Wallet.objects.get_or_create(owner=self.request.user)
        return wallet


class TransactionListView(ResponseMixin, generics.ListCreateAPIView):
    """
    Список транзакций + добавление новой.
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(wallet__owner=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        wallet = Wallet.objects.get(owner=self.request.user)
        create_transaction(wallet, serializer.validated_data)


class CategoryListView(ResponseMixin, generics.ListCreateAPIView):
    """
    Категории пользователя.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)
