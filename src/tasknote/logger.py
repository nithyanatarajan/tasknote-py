# src/tasknote/logger.py
import structlog

from src.common.logger import setup_logging
from src.tasknote.constants import service_name
from src.tasknote.settings import settings

setup_logging(service_name=service_name, log_level=settings.log_level)
log = structlog.get_logger()
