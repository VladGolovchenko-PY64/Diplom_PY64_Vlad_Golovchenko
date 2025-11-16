# apps/finance/views.py
from rest_framework import generics, permissions
from .models import Wallet, Transaction, Category
from .serializers import WalletSerializer, TransactionSerializer, CategorySerializer
from apps.core.mixins import ResponseMixin

class WalletListView(ResponseMixin, generics.ListCreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionListView(ResponseMixin, generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(wallet__owner=self.request.user).order_by("-date")

class CategoryListView(ResponseMixin, generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)
