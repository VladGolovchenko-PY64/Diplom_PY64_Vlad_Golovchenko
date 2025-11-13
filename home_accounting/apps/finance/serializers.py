# apps/finance/serializers.py
from rest_framework import serializers
from .models import Wallet, Transaction, Category


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wallet
        fields = ("id", "name", "balance", "currency", "owner")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "type", "is_important")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "wallet", "category", "amount", "comment", "date")
