"""
Lineups API module for the CFBD Python SDK.

This module provides an API wrapper for lineup-related endpoints.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import Endpoints
from cbbd.utils.cache import cached
from cbbd.utils.validation import validate_season
from cbbd.models.lineup import Lineup, LineupList
from .base import BaseAPI


class LineupsAPI(BaseAPI):
    """
    API wrapper for lineup-related endpoints.
    """
    
    def __init__(self, client):
        """
        Initialize the API wrapper.
        
        Args:
            client (CBBDClient): Client instance for API communication
        """
        super().__init__(client)
    
    @cached
    def get_lineups(
        self,
        game_id: Optional[int] = None,
        team: Optional[str] = None,
        season: Optional[int] = None,
        conference: Optional[str] = None,
        min_minutes: Optional[float] = None,
        min_possessions: Optional[int] = None
    ) -> LineupList:
        """
        Get lineup data.
        
        Args:
            game_id: Game ID filter
            team: Team name filter
            season: The season year (e.g., 2021)
            conference: Conference abbreviation filter
            min_minutes: Minimum minutes played filter
            min_possessions: Minimum possessions filter
            
        Returns:
            A LineupList object containing lineup data
        """
        params: Dict[str, Any] = {}
        
        if game_id is not None:
            params['gameId'] = game_id
            
        if team is not None:
            params['team'] = team
            
        if season is not None:
            validate_season(season)
            params['season'] = season
            
        if conference is not None:
            params['conference'] = conference
            
        if min_minutes is not None:
            params['minMinutes'] = min_minutes
            
        if min_possessions is not None:
            params['minPossessions'] = min_possessions
            
        response = Endpoints.make_request(Endpoints.LINEUPS, params)
        return LineupList(response) 