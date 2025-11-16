# apps/core/db/utils.py
def chunked_queryset(queryset, chunk_size=100):
    """
    Генератор, который возвращает элементы queryset порциями.
    """
    start = 0
    while True:
        chunk = queryset[start:start + chunk_size]
        if not chunk:
            break
        yield chunk
        start += chunk_size
