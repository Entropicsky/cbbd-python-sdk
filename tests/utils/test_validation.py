"""
Tests for validation utilities.
"""

import pytest
from datetime import datetime

from cbbd.exceptions import CBBDValidationError
from cbbd.utils.validation import (
    validate_required_params,
    validate_date,
    validate_season
)

class TestValidation:
    """Test validation utilities."""
    
    def test_validate_required_params(self):
        """Test required parameter validation."""
        # Test with all required params present
        params = {"foo": "bar", "baz": 123}
        validate_required_params(params, ["foo", "baz"])
        
        # Test with missing params
        with pytest.raises(CBBDValidationError):
            validate_required_params(params, ["foo", "qux"])
        
        # Test with None value
        params = {"foo": "bar", "baz": None}
        with pytest.raises(CBBDValidationError):
            validate_required_params(params, ["foo", "baz"])
    
    def test_validate_date(self):
        """Test date validation."""
        # Test valid ISO 8601 formats
        valid_dates = [
            "2023-01-01T12:30:45",
            "2023-01-01T12:30:45Z",
            "2023-01-01T12:30:45+00:00",
            "2023-01-01"
        ]
        for date in valid_dates:
            validate_date(date)
        
        # Test invalid formats
        invalid_dates = [
            "01/01/2023",
            "2023/01/01",
            "not a date",
            "2023-13-01"  # Invalid month
        ]
        for date in invalid_dates:
            with pytest.raises(CBBDValidationError):
                validate_date(date)
    
    def test_validate_season(self):
        """Test season validation."""
        # Test valid seasons
        valid_seasons = [2020, "2020", 1950]
        for season in valid_seasons:
            validate_season(season)
        
        # Test invalid seasons
        with pytest.raises(CBBDValidationError):
            validate_season(1800)  # Too early
        
        with pytest.raises(CBBDValidationError):
            validate_season(2200)  # Too far in future
        
        with pytest.raises(CBBDValidationError):
            validate_season("not a season") 