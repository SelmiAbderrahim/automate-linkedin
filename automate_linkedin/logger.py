from loguru import logger as logging
from decouple import config, UndefinedValueError

try:
    debug = config("BACKTRACE")
except UndefinedValueError:
    debug = 0
logging.add(
    "logs/debug-{time:YYYY-MM-DD}.log",
    format=(
        "<green>{time:YYYY-MM-DD}</green> "
        "| <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
    level="INFO",
    colorize=True,
    rotation="10 MB",
    retention="10 days",
    backtrace=True if debug else False,
    diagnose=True if debug else False,
)
