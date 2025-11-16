# apps/finance/serializers.py
from rest_framework import serializers
from .models import Wallet, Category, Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("id", "name", "balance", "currency", "owner")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "type", "is_important")

class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ("id", "wallet", "category", "amount", "comment", "date", "type")

    def get_type(self, obj):
        return obj.category.type if obj.category else None
