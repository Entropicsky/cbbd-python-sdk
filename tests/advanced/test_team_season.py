"""
Tests for the advanced team season functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from cbbd.advanced.team_season import TeamSeasonProfile


class TestTeamSeasonProfile:
    """Tests for the TeamSeasonProfile class."""
    
    def test_initialization(self, mock_client):
        """Test initialization of TeamSeasonProfile."""
        profile = TeamSeasonProfile(mock_client)
        assert profile.client == mock_client
    
    def test_get_profile(self, mock_client):
        """Test get_profile method."""
        # Set up mock responses for all the API calls
        teams_mock = MagicMock()
        teams_mock.to_dict.return_value = {'id': 1, 'name': 'Duke', 'conference': 'ACC'}
        
        roster_mock = MagicMock()
        roster_mock.to_dict.return_value = {'teamId': 1, 'team': 'Duke', 'season': 2023, 'players': []}
        
        games_mock = MagicMock()
        games_mock.to_dict.return_value = {'id': 1, 'home_team': 'Duke', 'away_team': 'UNC'}
        
        stats_mock = MagicMock()
        stats_mock.to_dict.return_value = {'team': 'Duke', 'points': 80}
        
        rankings_mock = MagicMock()
        rankings_mock.week = 1
        poll_mock = MagicMock()
        poll_mock.poll = 'AP Top 25'
        rank_mock = MagicMock()
        rank_mock.school = 'Duke'
        rank_mock.rank = 1
        poll_mock.ranks = [rank_mock]
        rankings_mock.polls = [poll_mock]
        
        srs_mock = MagicMock()
        srs_mock.to_dict.return_value = {'team': 'Duke', 'rating': 10.5}
        
        # Mock the API calls
        mock_client.teams.get_teams.return_value = [teams_mock]
        mock_client.teams.get_roster.return_value = roster_mock
        mock_client.games.get_games.return_value = [games_mock]
        mock_client.stats.get_team_stats.return_value = [stats_mock]
        mock_client.rankings.get_rankings.return_value = [rankings_mock]
        mock_client.ratings.get_srs_ratings.return_value = [srs_mock]
        
        # Test the method
        profile = TeamSeasonProfile(mock_client)
        result = profile.get_profile(team='Duke', season=2023)
        
        # Verify the result
        assert isinstance(result, dict)
        assert 'team' in result
        assert 'roster' in result
        assert 'games' in result
        assert 'stats' in result
        assert 'rankings' in result
        assert 'ratings' in result
        
        # Verify the API calls
        mock_client.teams.get_teams.assert_called_once_with(team='Duke')
        mock_client.teams.get_roster.assert_called_once_with(team='Duke', season=2023)
        mock_client.games.get_games.assert_called_once()
        mock_client.stats.get_team_stats.assert_called_once()
        mock_client.rankings.get_rankings.assert_called_once()
        mock_client.ratings.get_srs_ratings.assert_called_once()
    
    @pytest.mark.integration
    def test_get_profile_integration(self, client):
        """Integration test for get_profile method."""
        # Skip if no API key is available
        if not client:
            pytest.skip("No API key available for integration tests")
        
        # Test the method
        profile = TeamSeasonProfile(client)
        result = profile.get_profile(team='Duke', season=2023)
        
        # Verify the result structure
        assert isinstance(result, dict)
        assert 'team' in result
        assert 'roster' in result
        assert 'games' in result
        assert 'stats' in result
        assert 'rankings' in result
        assert 'ratings' in result 