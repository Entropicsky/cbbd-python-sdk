"""
Tests for the Teams API.
"""

import pytest
import responses
from cbbd.constants import Endpoints
from cbbd.models.team import Team, TeamList, TeamRoster


class TestTeamsAPI:
    """Tests for the Teams API."""
    
    @responses.activate
    def test_get_teams(self, mock_client, register_mock_endpoints):
        """Test getting teams."""
        # Register mock endpoint
        mock_data = register_mock_endpoints(Endpoints.TEAMS, 'teams.json')
        
        # Make the request
        teams = mock_client.teams.get_teams()
        
        # Verify the response
        assert isinstance(teams, TeamList)
        assert len(teams) == len(mock_data)
        
        # Verify the data
        for i, team in enumerate(teams):
            assert isinstance(team, Team)
            assert team.id == mock_data[i]['id']
            assert team.name == mock_data[i]['name']
            assert team.conference == mock_data[i]['conference']
    
    @responses.activate
    def test_get_teams_with_filters(self, mock_client, register_mock_endpoints):
        """Test getting teams with filters."""
        # Register mock endpoint with filters
        params = {'conference': 'ACC', 'season': 2023}
        mock_data = register_mock_endpoints(Endpoints.TEAMS, 'teams.json', params=params)
        
        # Make the request
        teams = mock_client.teams.get_teams(conference='ACC', season=2023)
        
        # Verify the response
        assert isinstance(teams, TeamList)
        assert len(teams) == len(mock_data)
    
    @responses.activate
    def test_get_roster(self, mock_client, register_mock_endpoints):
        """Test getting team roster."""
        # Register mock endpoint
        params = {'team': 'Duke', 'season': 2023}
        mock_data = register_mock_endpoints(Endpoints.TEAMS_ROSTER, 'team_roster.json', params=params)
        
        # Make the request
        roster = mock_client.teams.get_roster(team='Duke', season=2023)
        
        # Verify the response
        assert isinstance(roster, TeamRoster)
        assert roster.team == 'Duke'
        assert roster.season == 2023
        assert len(roster.players) == len(mock_data)
        
        # Verify player data
        for i, player in enumerate(roster.players):
            assert player.id == mock_data[i]['id']
            assert player.name == mock_data[i]['name']
            assert player.position == mock_data[i]['position']
            assert player.jersey == mock_data[i]['jersey']
    
    @pytest.mark.integration
    def test_get_teams_integration(self, client):
        """Integration test for getting teams."""
        # Skip if no API key is available
        if not client:
            pytest.skip("No API key available for integration tests")
        
        # Make the request
        teams = client.teams.get_teams()
        
        # Verify the response
        assert isinstance(teams, TeamList)
        assert len(teams) > 0
        
        # Verify the data structure
        team = teams[0]
        assert isinstance(team, Team)
        assert team.id is not None
        assert team.name is not None
    
    @pytest.mark.integration
    def test_get_roster_integration(self, client):
        """Integration test for getting team roster."""
        # Skip if no API key is available
        if not client:
            pytest.skip("No API key available for integration tests")
        
        # Make the request
        roster = client.teams.get_roster(team='Duke', season=2023)
        
        # Verify the response
        assert isinstance(roster, TeamRoster)
        assert roster.team == 'Duke'
        assert roster.season == 2023
        
        # Only verify if we got players
        if roster.players:
            player = roster.players[0]
            assert player.id is not None
            assert player.name is not None 