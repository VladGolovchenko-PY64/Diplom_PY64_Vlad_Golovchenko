# apps/core/utils/helpers.py
import logging

logger = logging.getLogger(__name__)

def log_action(user, action, extra=None):
    """
    Записывает действие пользователя в лог.
    """
    logger.info(f"[USER {user}] {action} | extra={extra}")
