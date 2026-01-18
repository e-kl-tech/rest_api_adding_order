"""
Модуль: /config.py
Описание: 
Автор: Евгений Климов
Дата создания: 2026-01-18
Лицензия: MIT License

Copyright (C) 2026 Evgenii Klimov
"""
__author__ = "Evgenii Klimov"
__license__ = "MIT"

import logging
import sys
import threading
import yaml

from datetime import datetime
from pathlib import Path


logger = logging.getLogger(__name__)

class _Setting:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._data = {}
        self._config_path = None
        self._last_modified = None
        self._initialized = True

    def load(self, config_path: str) -> None:
        """Загрузка или перезагрузка конфигурации"""
        self._config_path = Path(config_path)
        self._reload()

    def _reload(self) -> None:
        """Перезагрузка конфигурации из файла"""
        if not self._config_path or not self._config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self._config_path}")

        with open(self._config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        self._data = self._dict_to_object(data)
        self._last_modified = datetime.now()

    def _dict_to_object(self, data: dict[str, ...]) -> ...:
        """Рекурсивное преобразование dict в объекты"""
        if isinstance(data, dict):
            obj = type('Setting', (), {})()
            for key, value in data.items():
                setattr(obj, key, self._dict_to_object(value))
            return obj
        elif isinstance(data, list):
            return [self._dict_to_object(item) for item in data]
        else:
            return data

    def __getattr__(self, name: str) -> ...:
        # Проверяем обновление файла
        if self._config_path and self._config_path.exists():
            current_mtime = self._config_path.stat().st_mtime
            if self._last_modified is None or current_mtime > self._last_modified.timestamp():
                self._reload()

        if hasattr(self._data, name):
            return getattr(self._data, name)

        raise AttributeError(f"'{name}' не найдено")

    def reload(self) -> None:
        """Принудительная перезагрузка конфигурации"""
        if self._config_path:
            self._reload()

setting = _Setting()
try:
    setting.load('setting.yaml')
except FileNotFoundError:
    logger.warning("Ошибка конфигурирования:", exc_info=True)
    logger.error("Выход")
    sys.exit(1)

logging.basicConfig(
    level=setting.logger.level,
    format=setting.logger.format,
    datefmt=setting.logger.datefmt
)
for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    logging.getLogger(logger_name).handlers = []
    logging.getLogger(logger_name).propagate = True
logger.info("Инициализация конфига: ОК")
