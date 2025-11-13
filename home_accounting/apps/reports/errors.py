# apps/reports/errors.py
from apps.core.exceptions.logic_exceptions import LogicError

class ReportNotReadyError(LogicError):
    message = "Отчёт ещё не готов, попробуйте позже."
