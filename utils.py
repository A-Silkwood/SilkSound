import logging
import logging.handlers

from dotenv import dotenv_values
import os


config = dotenv_values(".env")


def init_logger():
    global logger
    
    # check for directory
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # initialize discord.py logger
    handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(os.getcwd(), "logs", f"{config.get('PROJECT_NAME')}.log"),
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}{message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(config.get('PROJECT_NAME'))
    logger.setLevel(logging.DEBUG if config.get("ENV") == "dev" else logging.INFO)
    logger.addHandler(handler)
    
    logger.info("Started bot")
