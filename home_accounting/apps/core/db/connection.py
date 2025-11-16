# apps/core/db/connection.py
from django.db import connection

def execute_raw(sql, params=None):
    """
    Выполнение "сырого" SQL-запроса.
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        return None
