"""
Lines API module for the CBBD Python SDK.

This module provides an API wrapper for betting lines related endpoints.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import Endpoints, SeasonTypes
from cbbd.utils.cache import cached
from cbbd.utils.validation import validate_season, validate_date
from cbbd.models.line import Line, LineList
from .base import BaseAPI


class LinesAPI(BaseAPI):
    """
    API wrapper for betting lines related endpoints.
    """
    
    @cached
    def get_lines(
        self,
        game_id: Optional[int] = None,
        season: Optional[int] = None,
        season_type: str = SeasonTypes.REGULAR,
        team: Optional[str] = None,
        conference: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> LineList:
        """
        Get betting lines.
        
        Args:
            game_id: Game ID filter
            season: The season year (e.g., 2021)
            season_type: Season type filter (regular, postseason, or both)
            team: Team name filter
            conference: Conference abbreviation filter
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            
        Returns:
            A LineList object containing betting lines
        """
        params: Dict[str, Any] = {
            'seasonType': season_type
        }
        
        if game_id is not None:
            params['gameId'] = game_id
            
        if season is not None:
            validate_season(season)
            params['season'] = season
            
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        if start_date is not None:
            validate_date(start_date)
            params['startDateRange'] = start_date
            
        if end_date is not None:
            validate_date(end_date)
            params['endDateRange'] = end_date
            
        response = self._request(Endpoints.LINES, params)
        return LineList(response) 