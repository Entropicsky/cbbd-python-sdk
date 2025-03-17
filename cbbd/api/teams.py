"""
Teams API for the CFBD Python SDK.
"""

from ..constants import Endpoints
from ..utils.cache import cached
from ..utils.validation import validate_season
from ..models.team import Team, TeamList, TeamRoster
from .base import BaseAPI

class TeamsAPI(BaseAPI):
    """API wrapper for team-related endpoints."""
    
    @cached
    def get_teams(self, conference=None, season=None):
        """
        Get team information.
        
        Args:
            conference (str, optional): Conference abbreviation filter
            season (int, optional): Season filter
            
        Returns:
            TeamList: List of Team objects
        """
        params = {}
        
        if conference:
            params['conference'] = conference
            
        if season:
            params['season'] = validate_season(season)
            
        data = self._request(Endpoints.TEAMS, params)
        return TeamList(data)
    
    @cached
    def get_roster(self, team, season):
        """
        Get team roster.
        
        Args:
            team (str): Team name
            season (int): Season
            
        Returns:
            TeamRoster: Team roster object
        """
        params = {
            'team': team,
            'season': validate_season(season)
        }
        
        data = self._request(Endpoints.TEAMS_ROSTER, params)
        
        # The API returns a list of players, but we want to structure it as a roster
        roster_data = {
            'teamId': None,  # We don't have this in the response
            'team': team,
            'season': season,
            'players': data
        }
        
        return TeamRoster(roster_data) 