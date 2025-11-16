# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "is_parent", "is_staff")
    list_filter = ("is_parent", "is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("gender", "avatar", "is_parent")}),
    )
