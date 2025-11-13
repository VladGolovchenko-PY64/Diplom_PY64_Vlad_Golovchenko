# apps/core/utils/validators.py
import re
from django.core.exceptions import ValidationError

def validate_username(value):
    """
    Проверяет имя пользователя (латиница, цифры, подчёркивания, 3–30 символов)
    """
    if len(value) < 3:
        raise ValidationError("Имя пользователя должно содержать не менее 3 символов.")
    if len(value) > 30:
        raise ValidationError("Имя пользователя не может превышать 30 символов.")
    if not re.match(r"^[A-Za-z0-9_]+$", value):
        raise ValidationError("Имя пользователя может содержать только буквы, цифры и подчёркивания.")
