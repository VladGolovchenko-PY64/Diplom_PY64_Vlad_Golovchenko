# apps/core/db/connection.py
from django.db import connections, OperationalError

def check_db_connection(alias="default") -> bool:
    """
    Проверка соединения с базой данных.
    Возвращает True, если соединение успешно, иначе False.
    """
    try:
        connection = connections[alias]
        connection.cursor()
        return True
    except OperationalError:
        return False
