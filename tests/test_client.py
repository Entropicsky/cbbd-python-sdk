"""
Tests for the CFBD client initialization and API property access.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from cbbd import CBBDClient
from cbbd.exceptions import CBBDError


class TestCBBDClient:
    """Tests for the CBBDClient class."""
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = CBBDClient(api_key="test-api-key")
        assert client.api_key == "test-api-key"
        assert client.use_cache is True
        assert client.cache is not None
    
    def test_init_with_env_var(self):
        """Test initialization with environment variable."""
        with patch.dict(os.environ, {"CFBD_API_KEY": "env-api-key"}):
            client = CBBDClient()
            assert client.api_key == "env-api-key"
    
    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                CBBDClient()
    
    def test_init_with_cache_options(self):
        """Test initialization with cache options."""
        client = CBBDClient(api_key="test-api-key", use_cache=False)
        assert client.use_cache is False
        assert client.cache is None
        
        client = CBBDClient(api_key="test-api-key", cache_ttl=600)
        assert client.cache_ttl == 600
    
    def test_init_with_logging_options(self):
        """Test initialization with logging options."""
        import logging
        client = CBBDClient(
            api_key="test-api-key",
            log_level=logging.DEBUG,
            log_file="test.log"
        )
        assert client.logger.level == logging.DEBUG
    
    def test_api_property_access(self):
        """Test API property access."""
        client = CBBDClient(api_key="test-api-key")
        
        # Test each API property
        assert client.teams is not None
        assert client.games is not None
        assert client.conferences is not None
        assert client.venues is not None
        assert client.stats is not None
        assert client.rankings is not None
        assert client.ratings is not None
        assert client.plays is not None
        assert client.lines is not None
        assert client.lineups is not None
        assert client.draft is not None
        assert client.recruiting is not None
        assert client.substitutions is not None
        
        # Test advanced functionality
        assert client.advanced is not None
        assert client.advanced.team_season is not None
        assert client.advanced.player_season is not None
        assert client.advanced.game_analysis is not None
    
    def test_close(self):
        """Test close method."""
        client = CBBDClient(api_key="test-api-key")
        client.session = MagicMock()
        client.close()
        client.session.close.assert_called_once()
    
    @pytest.mark.integration
    def test_integration(self, client):
        """Integration test for client initialization and API access."""
        # Skip if no API key is available
        if not client:
            pytest.skip("No API key available for integration tests")
        
        # Test teams API
        teams = client.teams.get_teams()
        assert len(teams) > 0
        
        # Test conferences API
        conferences = client.conferences.get_conferences()
        assert len(conferences) > 0 