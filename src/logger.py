import logging
import sys


def get_logger() -> logging.Logger:
    """Provide a basic logging system displaying info to standard output."""
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)
