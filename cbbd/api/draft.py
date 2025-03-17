"""
Draft API module for the CFBD Python SDK.

This module provides an API wrapper for NBA draft related endpoints.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import Endpoints
from cbbd.utils.cache import cached
from cbbd.models.draft import DraftPick, DraftPickList
from .base import BaseAPI


class DraftAPI(BaseAPI):
    """
    API wrapper for NBA draft related endpoints.
    """
    
    def __init__(self, client):
        """
        Initialize the API wrapper.
        
        Args:
            client (CBBDClient): Client instance for API communication
        """
        super().__init__(client)
    
    @cached
    def get_draft_picks(
        self,
        year: Optional[int] = None,
        team: Optional[str] = None,
        conference: Optional[str] = None,
        nba_team: Optional[str] = None,
        position: Optional[str] = None,
        round_number: Optional[int] = None
    ) -> DraftPickList:
        """
        Get NBA draft picks.
        
        Args:
            year: Draft year filter
            team: College team name filter
            conference: College conference abbreviation filter
            nba_team: NBA team name filter
            position: Player position filter
            round_number: Draft round filter
            
        Returns:
            A DraftPickList object containing draft picks
        """
        params: Dict[str, Any] = {}
        
        if year is not None:
            params['year'] = year
            
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        if nba_team is not None:
            params['nbaTeam'] = nba_team
            
        if position is not None:
            params['position'] = position
            
        if round_number is not None:
            params['round'] = round_number
            
        response = Endpoints.make_request(Endpoints.DRAFT, params)
        return DraftPickList(response) 