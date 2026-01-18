"""
Конфигурация системы логирования.
Настройка вывода логов в консоль.
"""
import logging
import sys

from datetime import datetime

from config import setting

def setup_logging(log_level: str = setting.logger.level):
    """
    Настраивает систему логирования.
    
    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    log_format = logging.Formatter(
        fmt=setting.logger.format,
        datefmt=setting.logger.datefmt
    )
    
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    existing_handlers = root_logger.handlers[:]
    for handler in existing_handlers:
        if not (isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout):
            root_logger.removeHandler(handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(log_format)
    
    root_logger.addHandler(console_handler)
    
    logging.getLogger("uvicorn").setLevel(logging.CRITICAL)
    logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.CRITICAL)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Система логирования настроена. Уровень: {log_level}")
    
    return logger
