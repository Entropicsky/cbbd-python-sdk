"""
Recruiting API module for the CFBD Python SDK.

This module provides an API wrapper for recruiting-related endpoints.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import Endpoints
from cbbd.utils.cache import cached
from cbbd.models.recruiting import Recruit, RecruitList, TeamRecruitingRank, TeamRecruitingRankList
from .base import BaseAPI


class RecruitingAPI(BaseAPI):
    """
    API wrapper for recruiting-related endpoints.
    """
    
    def __init__(self, client):
        """
        Initialize the API wrapper.
        
        Args:
            client (CBBDClient): Client instance for API communication
        """
        super().__init__(client)
    
    @cached
    def get_recruits(
        self,
        year: int,
        team: Optional[str] = None,
        position: Optional[str] = None,
        state: Optional[str] = None,
        min_stars: Optional[int] = None
    ) -> RecruitList:
        """
        Get basketball recruits.
        
        Args:
            year: Recruiting class year
            team: Team name filter
            position: Position filter
            state: State filter
            min_stars: Minimum star rating filter
            
        Returns:
            A RecruitList object containing recruits
        """
        params: Dict[str, Any] = {
            'year': year
        }
        
        if team is not None:
            params['team'] = team
            
        if position is not None:
            params['position'] = position
            
        if state is not None:
            params['state'] = state
            
        if min_stars is not None:
            params['minStars'] = min_stars
            
        response = Endpoints.make_request(Endpoints.RECRUITING, params)
        return RecruitList(response)
    
    @cached
    def get_team_recruiting_rankings(
        self,
        year: int,
        team: Optional[str] = None,
        conference: Optional[str] = None
    ) -> TeamRecruitingRankList:
        """
        Get team recruiting rankings.
        
        Args:
            year: Recruiting class year
            team: Team name filter
            conference: Conference abbreviation filter
            
        Returns:
            A TeamRecruitingRankList object containing team recruiting rankings
        """
        params: Dict[str, Any] = {
            'year': year
        }
        
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        response = Endpoints.make_request(Endpoints.RECRUITING_RANKINGS, params)
        return TeamRecruitingRankList(response) 