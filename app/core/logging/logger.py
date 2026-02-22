import os, logging
from logging.handlers import RotatingFileHandler
from .formatter import JSONFormatter


class LoggingManager:

    @staticmethod
    def configure():
        logger = logging.getLogger("app")
        logger.setLevel(logging.INFO)

        os.makedirs("logs", exist_ok=True)

        formatter = JSONFormatter()

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(
            "logs/app.log",
            maxBytes=5_000_000,
            backupCount=5
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    @staticmethod
    def get_logger(name: str):
        return logging.getLogger("app." + name)
