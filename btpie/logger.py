logger_text = """import logging
import os

def setup_logger(logfile):
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    logger = logging.getLogger("btpie")
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
