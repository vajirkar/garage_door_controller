import logging
import time
from logging.handlers import RotatingFileHandler
import gdc_settings as config

def create_rotating_log():
    # Creates a rotating log
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = RotatingFileHandler(config.gdcLogfile, maxBytes=config.maxBytes, backupCount=config.backupCount)
    logger.addHandler(handler)
    return logger
