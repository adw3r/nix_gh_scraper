import logging
import sys

from loguru import logger

from gh_scraper import config

logger.remove()
logging.disable()
LOGGING_FORMAT = (
    "<level>{time:YYYY-MM-DD HH:mm:ss.SSS}</level> "
    "<level>{level}</level>: "
    "<level>{name}</level> - "
    "<level>{message}</level>"
)

logger.add(
    config.ROOT_DIR / "logs" / "log_{time:YYYY-MM-DD}.log",
    format=LOGGING_FORMAT,
    level="DEBUG",
    mode="a",
    retention="5 days",
)
logger.add(sys.stdout, format=LOGGING_FORMAT)
