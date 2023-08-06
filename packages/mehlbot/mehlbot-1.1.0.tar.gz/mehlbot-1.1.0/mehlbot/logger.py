"""The package's logger utility to set up a logger."""
import logging
from logging import Logger


def setup_logger(name: str) -> Logger:
    """Configures a new logger with handlers and formatters.

    :param name: name of the logger (__name__)
    :return: configured logger.
    """
    logging.basicConfig()

    stream_handler = (logging.StreamHandler(),)
    file_handler = logging.FileHandler("debug.log", encoding="utf-8")
    output_format: logging.Formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    stream_handler[0].setFormatter(output_format)
    file_handler.setFormatter(output_format)

    logger = logging.getLogger(name)
    logger.setLevel(level=logging.DEBUG)

    logger.addHandler(file_handler)

    return logger
