# MIT License - Copyright (c) 2025 Robert Cole

import logging
import os
from btpie.logger import setup_logger

def test_logger_initialization(tmp_path):
    """Test that logger creates a valid file and logs to it."""
    log_file = tmp_path / "test.log"
    logger = setup_logger(log_file=str(log_file), verbose=False)
    
    assert isinstance(logger, logging.Logger)
    logger.info("Logger initialized successfully")

    logger.handlers[0].flush()
    assert log_file.exists()
    contents = log_file.read_text()
    assert "Logger initialized successfully" in contents

def test_logger_multiple_messages(tmp_path):
    """Test logger writes multiple messages to the file."""
    log_file = tmp_path / "multi.log"
    logger = setup_logger(log_file=str(log_file), verbose=False)

    messages = ["First message", "Second message", "Third message"]
    for msg in messages:
        logger.debug(msg)

    for handler in logger.handlers:
        handler.flush()

    assert log_file.exists()
    log_output = log_file.read_text()
    for msg in messages:
        assert msg in log_output