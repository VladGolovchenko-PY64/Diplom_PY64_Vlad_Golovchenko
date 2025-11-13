# apps/users/permissions.py
from rest_framework import permissions

class IsParent(permissions.BasePermission):
    """
    Доступ только для родителей.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_parent
