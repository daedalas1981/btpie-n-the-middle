# MIT License - Copyright (c) 2025 Robert Cole

import logging
from btpie.logger import setup_logger

def test_logger_initialization(tmp_path):
    """Test that logger creates a valid file and logs to it."""
    log_file = tmp_path / "test.log"
    logger = setup_logger(str(log_file), verbose=False)

    assert logger is not None
    logger.info("Test log message")

    assert log_file.exists()
    with open(log_file, "r") as f:
        contents = f.read()
        assert "Test log message" in contents

def test_logger_multiple_messages(tmp_path):
    """Test logger writes multiple lines to file."""
    log_file = tmp_path / "multi.log"
    logger = setup_logger(str(log_file), verbose=False)

    logger.info("First message")
    logger.info("Second message")

    with open(log_file, "r") as f:
        contents = f.read()
        lines = contents.strip().split("\n")
        assert "First message" in contents
        assert "Second message" in contents
        assert len(lines) >= 2