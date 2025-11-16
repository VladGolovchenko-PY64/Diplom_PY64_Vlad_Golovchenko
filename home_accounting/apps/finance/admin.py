from django.contrib import admin
from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'balance', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('owner__username',)

    @staticmethod
    def owner(obj):
        return obj.owner_wallet.username
