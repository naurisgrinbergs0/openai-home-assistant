import settings as s
import logging
from utility import config

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(config.get_data_file_path("LOG_FILE_NAME"))
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)


# Debug message
def d(message, print_to_console=False):
    if s.system["LOGGING_ENABLED"]:
        logger.debug(message)
        if print_to_console:
            print(message)


# Info message
def i(message, print_to_console=False):
    if s.system["LOGGING_ENABLED"]:
        logger.info(message)
        if print_to_console:
            print(message)


# Error message
def e(message, print_to_console=False):
    if s.system["LOGGING_ENABLED"]:
        logger.error(message)
        if print_to_console:
            print(message)
