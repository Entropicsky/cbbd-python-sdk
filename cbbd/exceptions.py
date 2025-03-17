"""
Custom exceptions for the CBBD Python SDK.
"""

class CBBDError(Exception):
    """Base exception for CBBD API errors."""
    pass

class CBBDAuthError(CBBDError):
    """
    Authentication error.
    
    Raised when the API key is invalid or missing.
    """
    pass

class CBBDRateLimitError(CBBDError):
    """
    Rate limit exceeded error.
    
    Raised when the API rate limit is exceeded.
    """
    pass

class CBBDNotFoundError(CBBDError):
    """
    Resource not found error.
    
    Raised when the requested resource is not found.
    """
    pass

class CBBDAPIError(CBBDError):
    """
    General API error.
    
    Raised for other API errors not covered by specific exceptions.
    """
    pass

class CBBDValidationError(CBBDError):
    """
    Input validation error.
    
    Raised when input parameters fail validation.
    """
    pass 