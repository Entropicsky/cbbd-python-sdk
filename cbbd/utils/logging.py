"""
Logging utilities for the CFBD Python SDK.
"""

import logging
import os
import sys
from typing import Optional, Union, TextIO


def setup_logger(
    name: str = "cfbd",
    level: Union[int, str] = logging.INFO,
    log_format: Optional[str] = None,
    log_file: Optional[str] = None,
    stream: Optional[TextIO] = sys.stdout
) -> logging.Logger:
    """
    Set up a logger for the CFBD SDK.
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
        log_format: Log message format (default: None, uses a standard format)
        log_file: Path to log file (default: None, logs to console only)
        stream: Stream to log to (default: sys.stdout)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Set default format if not provided
    if log_format is None:
        log_format = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
    
    formatter = logging.Formatter(log_format)
    
    # Add console handler
    console_handler = logging.StreamHandler(stream)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if log_file is provided
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Default logger
logger = setup_logger()


def get_logger(name: str = "cfbd") -> logging.Logger:
    """
    Get a logger for the CFBD SDK.
    
    Args:
        name: Logger name (default: "cfbd")
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name) 