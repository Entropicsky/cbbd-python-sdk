"""
Stats API module for the CBBD Python SDK.

This module provides an API wrapper for stats-related endpoints.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import Endpoints, SeasonTypes
from cbbd.utils.cache import cached
from cbbd.utils.validation import validate_season, validate_date
from cbbd.models.stats import (
    TeamStats, TeamStatsList, PlayerStats, PlayerStatsList, 
    AdvancedTeamStats, AdvancedTeamStatsList
)
from .base import BaseAPI


class StatsAPI(BaseAPI):
    """
    API wrapper for stats-related endpoints.
    """
    
    @cached
    def get_team_stats(
        self,
        season: Optional[int] = None,
        team: Optional[str] = None,
        conference: Optional[str] = None,
        game_id: Optional[int] = None,
        season_type: str = SeasonTypes.REGULAR,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> TeamStatsList:
        """
        Get team statistics.
        
        Args:
            season: The season year (e.g., 2021)
            team: Team name filter
            conference: Conference abbreviation filter
            game_id: Game ID filter
            season_type: Season type filter (regular, postseason, or both)
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            
        Returns:
            A TeamStatsList object containing team statistics
        """
        params: Dict[str, Any] = {
            'seasonType': season_type
        }
        
        if season is not None:
            validate_season(season)
            params['season'] = season
            
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        if game_id is not None:
            params['gameId'] = game_id
            
        if start_date is not None:
            validate_date(start_date)
            params['startDate'] = start_date
            
        if end_date is not None:
            validate_date(end_date)
            params['endDate'] = end_date
            
        response = self._request(Endpoints.STATS_TEAM_SEASON, params)
        return TeamStatsList(response)
    
    @cached
    def get_player_season_stats(
        self,
        season: int,
        team: Optional[str] = None,
        conference: Optional[str] = None,
        player_id: Optional[int] = None,
        season_type: str = SeasonTypes.REGULAR,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> PlayerStatsList:
        """
        Get player season statistics.
        
        Args:
            season: The season year (e.g., 2021)
            team: Team name filter
            conference: Conference abbreviation filter
            player_id: Player ID filter
            season_type: Season type filter (regular, postseason, or both)
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            
        Returns:
            A PlayerStatsList object containing player statistics
        """
        params: Dict[str, Any] = {
            'season': validate_season(season),
            'seasonType': season_type
        }
        
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        if player_id is not None:
            params['athleteId'] = player_id
            
        if start_date is not None:
            validate_date(start_date)
            params['startDateRange'] = start_date
            
        if end_date is not None:
            validate_date(end_date)
            params['endDateRange'] = end_date
            
        response = self._request(Endpoints.STATS_PLAYER_SEASON, params)
        return PlayerStatsList(response)
    
    @cached
    def get_player_game_stats(
        self,
        game_id: Optional[int] = None,
        season: Optional[int] = None,
        team: Optional[str] = None,
        conference: Optional[str] = None,
        player_id: Optional[int] = None,
        season_type: str = SeasonTypes.REGULAR,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get player game statistics.
        
        Args:
            game_id: Game ID filter
            season: The season year (e.g., 2021)
            team: Team name filter
            conference: Conference abbreviation filter
            player_id: Player ID filter
            season_type: Season type filter (regular, postseason, or both)
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            
        Returns:
            A list of player game statistics
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
            
        if player_id is not None:
            params['athleteId'] = player_id
            
        if start_date is not None:
            validate_date(start_date)
            params['startDateRange'] = start_date
            
        if end_date is not None:
            validate_date(end_date)
            params['endDateRange'] = end_date
            
        return self._request(Endpoints.GAMES_PLAYERS, params)
    
    @cached
    def get_advanced_team_stats(
        self,
        season: int,
        team: Optional[str] = None,
        conference: Optional[str] = None,
        exclude_garbage_time: bool = False,
        start_week: Optional[int] = None,
        end_week: Optional[int] = None
    ) -> AdvancedTeamStatsList:
        """
        Get advanced team statistics.
        
        Args:
            season: The season year (e.g., 2021)
            team: Team name filter
            conference: Conference abbreviation filter
            exclude_garbage_time: Whether to exclude garbage time stats
            start_week: Start week filter
            end_week: End week filter
            
        Returns:
            An AdvancedTeamStatsList object containing advanced team statistics
        """
        validate_season(season)
        
        params: Dict[str, Any] = {
            'season': season,
            'excludeGarbageTime': exclude_garbage_time
        }
        
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        if start_week is not None:
            params['startWeek'] = start_week
            
        if end_week is not None:
            params['endWeek'] = end_week
            
        response = self._request(Endpoints.ADVANCED_TEAM_STATS, params)
        return AdvancedTeamStatsList(response) 