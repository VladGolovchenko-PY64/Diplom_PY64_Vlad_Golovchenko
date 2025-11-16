# apps/core/utils/helpers.py
import logging

logger = logging.getLogger(__name__)

def log_action(user, action, extra=None):
    logger.info("[USER %s] %s | extra=%s", getattr(user, "username", str(user)), action, extra)
