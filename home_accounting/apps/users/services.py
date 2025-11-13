# apps/users/services.py
from django.contrib.auth import get_user_model
from apps.core.exceptions.logic_exceptions import LogicError

User = get_user_model()

def create_family(owner, name):
    """
    Создание новой семьи.
    """
    if not owner.is_admin_user:
        raise LogicError("Только родитель может создать семью.")
    from .models import Family
    return Family.objects.create(owner=owner, name=name)
