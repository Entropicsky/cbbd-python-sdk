"""
Base API class for the CBBD Python SDK.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..constants import BASE_URL
from ..exceptions import (
    CBBDAuthError,
    CBBDRateLimitError,
    CBBDNotFoundError,
    CBBDAPIError
)
from ..utils.logging import get_logger

class BaseAPI:
    """
    Base class for API endpoint wrappers.
    
    Attributes:
        client (CBBDClient): Client instance for API communication
        logger (logging.Logger): Logger instance
    """
    
    def __init__(self, client):
        """
        Initialize the API wrapper.
        
        Args:
            client (CBBDClient): Client instance for API communication
        """
        self.client = client
        self.logger = get_logger(f"cbbd.api.{self.__class__.__name__.lower()}")
        self.logger.debug(f"Initializing {self.__class__.__name__}")
    
    def _request(self, endpoint, params=None):
        """
        Make a request to the API.
        
        Args:
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
        
        Returns:
            dict or list: Response data
        
        Raises:
            CBBDAuthError: If authentication fails
            CBBDRateLimitError: If rate limit is exceeded
            CBBDNotFoundError: If resource is not found
            CBBDAPIError: For other API errors
        """
        url = f"{BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.client.api_key}",
            "accept": "application/json"
        }
        
        self.logger.debug(f"Making request to {endpoint} with params: {params}")
        
        try:
            response = self.client.session.get(url, headers=headers, params=params)
            
            # Handle error responses
            if response.status_code == 401:
                self.logger.error(f"Authentication failed for {endpoint}")
                raise CBBDAuthError("Authentication failed. Check your API key.")
            elif response.status_code == 429:
                self.logger.error(f"Rate limit exceeded for {endpoint}")
                raise CBBDRateLimitError("Rate limit exceeded. Please wait before making more requests.")
            elif response.status_code == 404:
                self.logger.error(f"Resource not found: {endpoint}")
                raise CBBDNotFoundError(f"Resource not found: {endpoint}")
            elif response.status_code != 200:
                self.logger.error(f"API error: {response.status_code} - {response.text}")
                raise CBBDAPIError(f"API error: {response.status_code} - {response.text}")
            
            self.logger.debug(f"Request to {endpoint} successful")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error for {endpoint}: {str(e)}")
            raise CBBDAPIError(f"Request error: {str(e)}")

def create_http_client():
    """
    Create HTTP client with connection pooling and retries.
    
    Returns:
        requests.Session: Configured session
    """
    logger = get_logger("cbbd.http")
    logger.debug("Creating HTTP client")
    
    session = requests.Session()
    
    # Configure retries
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    
    # Configure connection pooling
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=100)
    session.mount('https://', adapter)
    
    logger.debug("HTTP client created with retries and connection pooling")
    return session 