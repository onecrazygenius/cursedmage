# logging_config.py

import logging

def setup_logging():
    # Create a logger
    logger = logging.getLogger('cursedmage')

    # Set the logging level to DEBUG
    logger.setLevel(logging.DEBUG)

    # Create a console handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter to define the log message format
    formatter = logging.Formatter('[%(levelname)s] %(filename)s:%(lineno)d - %(message)s')

    # Set the formatter for the handlers
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()