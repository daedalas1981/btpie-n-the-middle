# MIT License - Copyright (c) 2025 Robert Cole

import logging
import os

def setup_logger(logfile):
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    
    logger = logging.getLogger("btpie")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
