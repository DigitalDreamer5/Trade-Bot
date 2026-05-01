"""Logging configuration for the trading bot."""

import logging
import logging.handlers
from datetime import datetime
from pathlib import Path


def setup_logging(log_dir: str = "logs") -> None:
    """Set up logging configuration for the trading bot.

    Creates logs directory if it doesn't exist and configures:
    - File logging at DEBUG level with full detail
    - Console logging at INFO level for clean output

    Args:
        log_dir: Directory to store log files (default: "logs")
    """
    # Create logs directory if not present
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Format string for all handlers
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    # File handler (DEBUG level with all details)
    log_file = log_path / f"trading_bot_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler (INFO level for clean output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info(f"Logging initialized. File: {log_file}")
