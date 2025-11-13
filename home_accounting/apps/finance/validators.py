# apps/finance/validators.py
from rest_framework.exceptions import ValidationError

def validate_amount(value):
    if value <= 0:
        raise ValidationError("Сумма должна быть больше нуля.")
