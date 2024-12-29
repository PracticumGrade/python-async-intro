import logging
from logging import StreamHandler, Formatter
import sys

# Настройки логирования
LOGGER_LEVEL = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


class Logger:
    """Настройка логера."""

    @staticmethod
    def create(logger_name: str, logger_level: str) -> logging.Logger:
        """Метод для создания экземпляра логгера."""
        logger = logging.getLogger(logger_name)
        # Указываем обработчик логов
        handler = StreamHandler(stream=sys.stdout)
        # Создаем форматер
        handler.setFormatter(
            Formatter(fmt='%(asctime)s: [%(levelname)s] %(message)s'))
        logger.addHandler(handler)
        # Устанавливаем уровень, с которого логи будут сохраняться в файл
        try:
            logger.setLevel(LOGGER_LEVEL.get(logger_level))
            return logger
        except TypeError:
            raise TypeError('Задан неверный уровень логирования!')
