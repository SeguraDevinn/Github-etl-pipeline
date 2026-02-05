import logging
import sys
from typing import Optional

def get_logger(name: str, level: Optional[int] = logging.INFO) -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name: Name of the logger (usually __name__)
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """

    logger = logging.getLogger(name)
    
    # Prevent duplicate logs 
    if logger.handlers:
        return logger
    
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger