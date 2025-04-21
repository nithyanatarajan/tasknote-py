# src/notes/logger.py
import structlog

from src.common.logger import setup_logging
from src.notes.settings import settings

setup_logging(service_name='notes', log_level=settings.log_level)
log = structlog.get_logger()
