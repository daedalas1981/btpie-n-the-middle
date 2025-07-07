# MIT License - Copyright (c) 2025 Robert Cole

"""
Utility functions for BTPIE-N-THE-MIDDLE
"""

import time

def hex_dump(data):
    """
    Return hex string representation of byte data.
    """
    if not data:
        return ""
    return " ".join(f"{b:02X}" for b in data)


def timestamp():
    """
    Return current timestamp string in readable format.
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
