"""
Ratings API module for the CBBD Python SDK.

This module provides an API wrapper for ratings-related endpoints.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import Endpoints
from cbbd.utils.cache import cached
from cbbd.utils.validation import validate_season
from cbbd.models.rating import (
    SRSRating, SRSRatingList, SPRating, SPRatingList, 
    EloRating, EloRatingList
)
from .base import BaseAPI


class RatingsAPI(BaseAPI):
    """
    API wrapper for ratings-related endpoints.
    """
    
    @cached
    def get_srs_ratings(
        self,
        season: int,
        team: Optional[str] = None,
        conference: Optional[str] = None
    ) -> SRSRatingList:
        """
        Get Simple Rating System (SRS) ratings.
        
        Args:
            season: The season year (e.g., 2021)
            team: Team name filter
            conference: Conference abbreviation filter
            
        Returns:
            A SRSRatingList object containing SRS ratings
        """
        validate_season(season)
        
        params: Dict[str, Any] = {
            'season': season
        }
        
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        response = self._request(Endpoints.RATINGS_SRS, params)
        return SRSRatingList(response)
    
    @cached
    def get_adjusted_ratings(
        self,
        season: int,
        team: Optional[str] = None,
        conference: Optional[str] = None
    ) -> SPRatingList:
        """
        Get adjusted efficiency ratings.
        
        Args:
            season: The season year (e.g., 2021)
            team: Team name filter
            conference: Conference abbreviation filter
            
        Returns:
            A SPRatingList object containing adjusted efficiency ratings
        """
        validate_season(season)
        
        params: Dict[str, Any] = {
            'season': season
        }
        
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        response = self._request(Endpoints.RATINGS_ADJUSTED, params)
        return SPRatingList(response)
    
    @cached
    def get_sp_ratings(
        self,
        season: int,
        team: Optional[str] = None,
        conference: Optional[str] = None
    ) -> SPRatingList:
        """
        Get SP+ ratings.
        
        Args:
            season: The season year (e.g., 2021)
            team: Team name filter
            conference: Conference abbreviation filter
            
        Returns:
            A SPRatingList object containing SP+ ratings
        """
        validate_season(season)
        
        params: Dict[str, Any] = {
            'year': season
        }
        
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        response = self._request(Endpoints.SP_RATINGS, params)
        return SPRatingList(response)
    
    @cached
    def get_elo_ratings(
        self,
        season: int,
        team: Optional[str] = None,
        conference: Optional[str] = None,
        week: Optional[int] = None
    ) -> EloRatingList:
        """
        Get Elo ratings.
        
        Args:
            season: The season year (e.g., 2021)
            team: Team name filter
            conference: Conference abbreviation filter
            week: Week filter
            
        Returns:
            An EloRatingList object containing Elo ratings
        """
        validate_season(season)
        
        params: Dict[str, Any] = {
            'year': season
        }
        
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        if week is not None:
            params['week'] = week
            
        response = self._request(Endpoints.ELO_RATINGS, params)
        return EloRatingList(response) 