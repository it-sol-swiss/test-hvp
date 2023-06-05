import os
import logging
from datetime import datetime


class LoggerConfig:
    filename = None


def configure_logger(name='Log', filename=None, level=logging.DEBUG, terminal_output=False):
    if filename is None:
        filename = f'log.txt'

    # Change the path to hv-bApp directory
    log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'hv-bApp', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    filename = os.path.join(log_dir, filename)
    LoggerConfig.filename = filename

    logger = logging.getLogger(name)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler() if terminal_output else logging.FileHandler(filename)
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level)
    if not os.path.exists(filename):
        open(filename, 'a').close()  # create file if it doesn't exist

    return logger
