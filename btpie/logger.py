# MIT License - Copyright (c) 2025 Robert Cole

import os
from datetime import datetime

class Logger:
    def __init__(self, log_file="logs/session.log"):
        self.log_file = log_file
        # Ensure the log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

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
