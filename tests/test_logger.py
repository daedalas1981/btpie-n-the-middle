# MIT License - Copyright (c) 2025 Robert Cole

import os
from btpie.logger import setup_logger

def test_logger_initialization(tmp_path):
    log_file = tmp_path / "test.log"
    
    logger = setup_logger(str(log_file))
    
    assert logger is not None
    logger.info("Test log message")
    
    assert log_file.exists()
    with open(log_file, "r") as f:
        content = f.read()
        assert "Test log message" in content

def test_logger_multiple_messages(tmp_path):
    log_file = tmp_path / "multi.log"

    logger = setup_logger(str(log_file))

    logger.info("First message")
    logger.info("Second message")

    with open(log_file, "r") as f:
        lines = f.readlines()

    assert any("First message" in line for line in lines)
    assert any("Second message" in line for line in lines)
