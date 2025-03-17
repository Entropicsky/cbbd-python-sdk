"""
Tests for the logging utilities.
"""

import os
import pytest
import logging
import tempfile
from io import StringIO

from cbbd.utils.logging import (
    setup_logger,
    get_logger
)


class TestLogging:
    """Tests for the logging utilities."""
    
    def test_setup_logger_with_defaults(self):
        """Test setup_logger with default parameters."""
        logger = setup_logger()
        
        assert logger.name == "cfbd"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.StreamHandler)
    
    def test_setup_logger_with_custom_name(self):
        """Test setup_logger with custom name."""
        logger = setup_logger(name="test_logger")
        
        assert logger.name == "test_logger"
    
    def test_setup_logger_with_custom_level(self):
        """Test setup_logger with custom level."""
        logger = setup_logger(level=logging.DEBUG)
        
        assert logger.level == logging.DEBUG
    
    def test_setup_logger_with_custom_format(self):
        """Test setup_logger with custom format."""
        custom_format = "%(name)s - %(levelname)s - %(message)s"
        logger = setup_logger(log_format=custom_format)
        
        assert logger.handlers[0].formatter._fmt == custom_format
    
    def test_setup_logger_with_file(self):
        """Test setup_logger with log file."""
        # Create temporary file for testing
        with tempfile.NamedTemporaryFile(suffix='.log', delete=False) as temp_file:
            log_file = temp_file.name
        
        try:
            logger = setup_logger(log_file=log_file)
            
            assert len(logger.handlers) == 2
            assert any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)
            
            # Test writing to log file
            test_message = "Test log message"
            logger.info(test_message)
            
            with open(log_file, 'r') as f:
                content = f.read()
                assert test_message in content
        finally:
            # Clean up the temporary file
            os.unlink(log_file)
    
    def test_setup_logger_with_custom_stream(self):
        """Test setup_logger with custom stream."""
        stream = StringIO()
        logger = setup_logger(stream=stream)
        
        test_message = "Test log message"
        logger.info(test_message)
        
        stream_content = stream.getvalue()
        assert test_message in stream_content
    
    def test_get_logger(self):
        """Test get_logger function."""
        # Get logger with default name
        logger1 = get_logger()
        assert logger1.name == "cfbd"
        
        # Get logger with custom name
        logger2 = get_logger("custom_name")
        assert logger2.name == "custom_name"
        
        # Get existing logger
        logger3 = get_logger("custom_name")
        assert logger3 is logger2 