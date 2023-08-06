# -*- coding: utf-8 -*-
"""

This module presents all the necessary configuration for the loguru
logger. This logger is used in the entire application.

Attributes
----------
current_host : str
    The current host server running the application

IP: str
    The IP address IPv4 of the current server running the application.

"""
import socket
from supextend.config import Config


current_host = socket.gethostname()
IP = socket.gethostbyname(current_host)


class LoggingConfig:
    """A class setting the logger from the third party library `loguru`

    Attributes:
    -----------
    logger_format: str
        Holds the settings for formatting the logger messages.
        It adds the user used to modify or read items from  superset
        and the originating IP to the logs.
    logger: Logger
        The logger used for the rest of the app.
    """

    import sys
    from loguru import logger

    logger_format = (
        "<green>{time:%Y-%b-%d %H:%M:%S}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "{extra[ip]} {extra[user]} - <level>{message}</level>"
    )

    logger.configure(extra={"ip": IP, "user": current_host})
    logger.remove()
    logger.add(sys.stderr, format=logger_format, level=Config.log_level)
    logger = logger
