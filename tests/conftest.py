"""
Pytest configuration for the CBBD Python SDK tests.
"""

import os
import pytest
import responses
import json
from pathlib import Path
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch

from cbbd import CBBDClient
from cbbd.constants import BASE_URL

# Load environment variables from .env file
load_dotenv()

# API key for testing
API_KEY = os.getenv('CBBD_API_KEY')

# Directory for mock responses
MOCK_RESPONSE_DIR = Path(__file__).parent / 'mock_responses'


@pytest.fixture
def client():
    """
    Fixture for a real client instance with API key.
    
    Use this for integration tests against the real API.
    """
    if not API_KEY:
        pytest.skip("No API key available for integration tests")
    
    return CBBDClient(api_key=API_KEY)


@pytest.fixture
def mock_client():
    """
    Fixture for a mock client instance.
    
    This client does not make real API calls but uses mocked responses.
    """
    with patch('cbbd.api.base.create_http_client'):
        client = CBBDClient(api_key='mock-api-key')
        client.session = MagicMock()
        return client


@pytest.fixture
def mock_responses():
    """
    Fixture for mock API responses using the responses library.
    
    Use this for unit tests where you want to mock API responses.
    """
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def load_mock_response():
    """
    Fixture for loading mock responses from JSON files.
    
    Returns a function that loads and returns mock response data.
    """
    def _load_mock_response(filename):
        """
        Load mock response data from a JSON file.
        
        Args:
            filename: Name of the JSON file in the mock_responses directory
            
        Returns:
            The loaded JSON data
        """
        file_path = MOCK_RESPONSE_DIR / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Mock response file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    return _load_mock_response


@pytest.fixture
def register_mock_endpoints(mock_responses, load_mock_response):
    """
    Fixture for registering mock endpoints with the responses library.
    
    Returns a function that registers a mock endpoint for testing.
    """
    def _register_mock_endpoint(endpoint, response_file, status=200, params=None):
        """
        Register a mock endpoint for testing.
        
        Args:
            endpoint: API endpoint (e.g., '/teams')
            response_file: Name of the JSON file containing the mock response
            status: HTTP status code to return
            params: Query parameters for the request
            
        Returns:
            The registered mock response
        """
        url = f"{BASE_URL}{endpoint}"
        mock_data = load_mock_response(response_file)
        
        # Add the mock endpoint
        mock_responses.add(
            responses.GET,
            url,
            json=mock_data,
            status=status,
            match=[responses.matchers.query_param_matcher(params or {})]
        )
        
        return mock_data
    
    return _register_mock_endpoint 