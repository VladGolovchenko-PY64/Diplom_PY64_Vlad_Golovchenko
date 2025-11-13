# apps/core/db/utils.py
from functools import wraps
from django.db import transaction

def atomic_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with transaction.atomic():
            return func(*args, **kwargs)
    return wrapper

