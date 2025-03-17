"""
Validation utilities for the CFBD Python SDK.
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..exceptions import CBBDValidationError
from .logging import get_logger

logger = get_logger(__name__)

def validate_required_params(params: Dict[str, Any], required: List[str]) -> None:
    """
    Validate that required parameters are present and not None.
    
    Args:
        params: Dictionary of parameters
        required: List of required parameter names
    
    Raises:
        CBBDValidationError: If any required parameters are missing
    """
    missing = [param for param in required if param not in params or params[param] is None]
    if missing:
        logger.error(f"Missing required parameters: {missing}")
        raise CBBDValidationError(f"Missing required parameters: {', '.join(missing)}")

def validate_date(date_str: str) -> None:
    """
    Validate date format.
    
    Args:
        date_str: Date string in ISO 8601 format (YYYY-MM-DDTHH:MM:SS) or YYYY-MM-DD
    
    Raises:
        CBBDValidationError: If date format is invalid
    """
    # ISO 8601 format regex
    iso_pattern = r'^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:?\d{2})?)?$'
    
    # Simple date format (YYYY-MM-DD)
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    
    if not re.match(iso_pattern, date_str) and not re.match(date_pattern, date_str):
        logger.error(f"Invalid date format: {date_str}")
        raise CBBDValidationError(f"Invalid date format: {date_str}. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS) or YYYY-MM-DD.")

def validate_season(season: Any) -> int:
    """
    Validate season parameter.
    
    Args:
        season: Season year (integer or string that can be converted to integer)
    
    Returns:
        int: Validated season as an integer
    
    Raises:
        CBBDValidationError: If season is invalid
    """
    try:
        season_int = int(season)
        
        if season_int < 1900 or season_int > 2100:
            logger.error(f"Invalid season range: {season}")
            raise CBBDValidationError(f"Invalid season: {season}. Season should be a year between 1900 and 2100.")
        return season_int
    except ValueError:
        logger.error(f"Invalid season type: {season}")
        raise CBBDValidationError(f"Invalid season: {season}. Season should be a year (integer).") 