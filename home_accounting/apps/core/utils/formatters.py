# apps/core/utils/formatters.py
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

def format_money(amount: Decimal, currency: str = "RUB") -> str:
    if amount is None:
        return f"0.00 {currency}"
    q = Decimal("0.01")
    return f"{Decimal(amount).quantize(q, rounding=ROUND_HALF_UP)} {currency}"
