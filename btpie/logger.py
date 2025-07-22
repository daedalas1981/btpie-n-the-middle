# MIT License - Copyright (c) 2025 Robert Cole

# btpie/logger.py
import os
import logging
from datetime import datetime

class Logger:
    def __init__(self, log_file="logs/session.log"):
        self.log_file = log_file
        # Ensure the log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        # Clear log on startup
        with open(self.log_file, "w") as f:
            f.write(f"[{self.timestamp()}] Logger initialized.\n")

    def timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, direction, data):
        formatted = " ".join(f"{byte:02X}" for byte in data)
        entry = f"[{self.timestamp()}] {direction}: {formatted}\n"
        with open(self.log_file, "a") as f:
            f.write(entry)

def setup_logger(level=logging.INFO):
    """
    Configure and return a logger for btpie.
    """
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=level
    )
    return logging.getLogger("btpie")