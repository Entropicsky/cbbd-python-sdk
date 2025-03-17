"""
Plays API module for the CBBD Python SDK.

This module provides an API wrapper for play-by-play related endpoints.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import Endpoints
from cbbd.utils.cache import cached
from cbbd.utils.validation import validate_season, validate_date
from cbbd.models.play import Play, PlayList, PlayType, PlayTypeList
from .base import BaseAPI


class PlaysAPI(BaseAPI):
    """
    API wrapper for play-by-play related endpoints.
    """
    
    @cached
    def get_plays(
        self,
        game_id: int,
        shooting_plays_only: bool = False
    ) -> PlayList:
        """
        Get play-by-play data for a game.
        
        Args:
            game_id: The game ID
            shooting_plays_only: Whether to return only shooting plays
            
        Returns:
            A PlayList object containing play-by-play data
        """
        endpoint = Endpoints.PLAYS_GAME.format(game_id=game_id)
        
        params: Dict[str, Any] = {}
        if shooting_plays_only:
            params['shootingPlaysOnly'] = True
        
        response = self._request(endpoint, params)
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        if response and len(response) > 0:
            logger.info(f"Raw Play API response example (first item): {response[0]}")
            logger.info(f"Response keys: {response[0].keys() if response and len(response) > 0 and isinstance(response[0], dict) else 'No keys found'}")
        else:
            logger.info("Empty response from Plays API")
            
        return PlayList(response)
    
    @cached
    def get_plays_by_player(
        self,
        player_id: int,
        season: int,
        shooting_plays_only: bool = False
    ) -> PlayList:
        """
        Get plays for a specific player in a season.
        
        Args:
            player_id: The player ID
            season: The season year
            shooting_plays_only: Whether to return only shooting plays
            
        Returns:
            A PlayList object containing plays
        """
        endpoint = Endpoints.PLAYS_PLAYER.format(player_id=player_id)
        
        params: Dict[str, Any] = {
            'season': validate_season(season)
        }
        
        if shooting_plays_only:
            params['shootingPlaysOnly'] = True
        
        response = self._request(endpoint, params)
        return PlayList(response)
    
    @cached
    def get_plays_by_team(
        self,
        team: str,
        season: int,
        shooting_plays_only: bool = False
    ) -> PlayList:
        """
        Get plays for a specific team in a season.
        
        Args:
            team: The team name
            season: The season year
            shooting_plays_only: Whether to return only shooting plays
            
        Returns:
            A PlayList object containing plays
        """
        params: Dict[str, Any] = {
            'team': team,
            'season': validate_season(season)
        }
        
        if shooting_plays_only:
            params['shootingPlaysOnly'] = True
        
        response = self._request(Endpoints.PLAYS_TEAM, params)
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        if response and len(response) > 0:
            logger.info(f"Raw Play API response example (first item): {response[0]}")
            logger.info(f"Response keys: {response[0].keys() if response and len(response) > 0 and isinstance(response[0], dict) else 'No keys found'}")
        else:
            logger.info("Empty response from Plays API")
            
        return PlayList(response)
    
    @cached
    def get_play_types(self) -> PlayTypeList:
        """
        Get a list of play types.
        
        Returns:
            A PlayTypeList object containing play types
        """
        response = self._request(Endpoints.PLAYS_TYPES)
        return PlayTypeList(response)
    
    @cached
    def get_play_stats(
        self,
        game_id: int,
        play_type: Optional[str] = None,
        team: Optional[str] = None,
        player: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get play statistics for a game.
        
        Args:
            game_id: The game ID
            play_type: Play type filter
            team: Team name filter
            player: Player name filter
            
        Returns:
            A list of dictionaries containing play statistics
        """
        params: Dict[str, Any] = {
            'gameId': game_id
        }
        
        if play_type is not None:
            params['playType'] = play_type
            
        if team is not None:
            params['team'] = team
            
        if player is not None:
            params['player'] = player
            
        return self._request(Endpoints.PLAY_STATS, params)
    
    @cached
    def get_play_stats_by_season(
        self,
        season: int,
        team: Optional[str] = None,
        conference: Optional[str] = None,
        play_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get play statistics for a season.
        
        Args:
            season: The season year (e.g., 2021)
            team: Team name filter
            conference: Conference abbreviation filter
            play_type: Play type filter
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            
        Returns:
            A list of dictionaries containing play statistics
        """
        validate_season(season)
        
        params: Dict[str, Any] = {
            'season': season
        }
        
        if team is not None:
            params['team'] = team
            
        if conference is not None:
            params['conference'] = conference
            
        if play_type is not None:
            params['playType'] = play_type
            
        if start_date is not None:
            validate_date(start_date)
            params['startDate'] = start_date
            
        if end_date is not None:
            validate_date(end_date)
            params['endDate'] = end_date
            
        return self._request(Endpoints.PLAY_STATS_SEASON, params) 