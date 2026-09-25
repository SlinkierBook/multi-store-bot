import logging
from logging.handlers import RotatingFileHandler


def configure_log():
    handler = RotatingFileHandler(
        "/app/logs/bot.log",
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding="utf-8",
    )
    
    logging.basicConfig(
        handlers=[handler],
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )