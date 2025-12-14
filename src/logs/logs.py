import logging

from config import (
    app_name,
    log_level
)


class Logs(object):
    def __init__(self, logger_name):
        # Логгер
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)

        # Формат логгов
        self.formatter = logging.Formatter(f'[{app_name} %(asctime)s] %(message)s')
        # Настроки консольного логгера
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)

        # Добавляем в логгер настройки
        if not self.logger.handlers:
            self.logger.addHandler(self.console_handler)
