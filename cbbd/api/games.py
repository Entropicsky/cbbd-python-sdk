"""
Games API for the CBBD Python SDK.
"""

from ..constants import Endpoints, SeasonTypes
from ..utils.cache import cached
from ..utils.validation import validate_season, validate_date
from ..models.game import Game, GameList, GameMedia, GameMediaList
from .base import BaseAPI

class GamesAPI(BaseAPI):
    """API wrapper for game-related endpoints."""
    
    @cached
    def get_game(self, game_id):
        """
        Get information for a specific game by ID.
        
        Args:
            game_id (int): Game ID
            
        Returns:
            Game: Game object
        """
        params = {'id': game_id}
        data = self._request(Endpoints.GAMES, params)
        
        # API returns a list, but we want a single game
        if data and isinstance(data, list) and len(data) > 0:
            return Game(data[0])
        return None
    
    @cached
    def get_games(self, season=None, team=None, conference=None, 
                  start_date=None, end_date=None, season_type=None):
        """
        Get game information.
        
        Args:
            season (int, optional): Season filter
            team (str, optional): Team name filter
            conference (str, optional): Conference abbreviation filter
            start_date (str or datetime, optional): Start date filter (ISO 8601 format)
            end_date (str or datetime, optional): End date filter (ISO 8601 format)
            season_type (str, optional): Season type filter ('regular', 'postseason', 'preseason')
            
        Returns:
            GameList: List of Game objects
        """
        params = {}
        
        if season:
            params['season'] = validate_season(season)
            
        if team:
            params['team'] = team
            
        if conference:
            params['conference'] = conference
            
        if start_date:
            params['startDateRange'] = validate_date(start_date)
            
        if end_date:
            params['endDateRange'] = validate_date(end_date)
            
        if season_type:
            if season_type not in [SeasonTypes.REGULAR, SeasonTypes.POSTSEASON, SeasonTypes.PRESEASON]:
                raise ValueError(f"Invalid season_type: {season_type}. Must be one of: 'regular', 'postseason', 'preseason'")
            params['seasonType'] = season_type
            
        data = self._request(Endpoints.GAMES, params)
        return GameList(data)
    
    @cached
    def get_media(self, season=None, team=None, conference=None, 
                  start_date=None, end_date=None, season_type=None):
        """
        Get game media information.
        
        Args:
            season (int, optional): Season filter
            team (str, optional): Team name filter
            conference (str, optional): Conference abbreviation filter
            start_date (str or datetime, optional): Start date filter (ISO 8601 format)
            end_date (str or datetime, optional): End date filter (ISO 8601 format)
            season_type (str, optional): Season type filter ('regular', 'postseason', 'preseason')
            
        Returns:
            GameMediaList: List of GameMedia objects
        """
        params = {}
        
        if season:
            params['season'] = validate_season(season)
            
        if team:
            params['team'] = team
            
        if conference:
            params['conference'] = conference
            
        if start_date:
            params['startDateRange'] = validate_date(start_date)
            
        if end_date:
            params['endDateRange'] = validate_date(end_date)
            
        if season_type:
            if season_type not in [SeasonTypes.REGULAR, SeasonTypes.POSTSEASON, SeasonTypes.PRESEASON]:
                raise ValueError(f"Invalid season_type: {season_type}. Must be one of: 'regular', 'postseason', 'preseason'")
            params['seasonType'] = season_type
            
        data = self._request(Endpoints.GAMES_MEDIA, params)
        return GameMediaList(data)
    
    @cached
    def get_team_stats(self, game_id=None, season=None, team=None, conference=None, 
                       start_date=None, end_date=None, season_type=None):
        """
        Get team box score statistics.
        
        Args:
            game_id (int, optional): Game ID filter
            season (int, optional): Season filter
            team (str, optional): Team name filter
            conference (str, optional): Conference abbreviation filter
            start_date (str or datetime, optional): Start date filter (ISO 8601 format)
            end_date (str or datetime, optional): End date filter (ISO 8601 format)
            season_type (str, optional): Season type filter ('regular', 'postseason', 'preseason')
            
        Returns:
            list: List of team statistics
        """
        params = {}
        
        if game_id:
            params['gameId'] = game_id
            
        if season:
            params['season'] = validate_season(season)
            
        if team:
            params['team'] = team
            
        if conference:
            params['conference'] = conference
            
        if start_date:
            params['startDateRange'] = validate_date(start_date)
            
        if end_date:
            params['endDateRange'] = validate_date(end_date)
            
        if season_type:
            if season_type not in [SeasonTypes.REGULAR, SeasonTypes.POSTSEASON, SeasonTypes.PRESEASON]:
                raise ValueError(f"Invalid season_type: {season_type}. Must be one of: 'regular', 'postseason', 'preseason'")
            params['seasonType'] = season_type
            
        return self._request(Endpoints.GAMES_TEAMS, params)
    
    @cached
    def get_player_stats(self, game_id=None, season=None, team=None, conference=None, 
                         start_date=None, end_date=None, season_type=None):
        """
        Get player box score statistics.
        
        Args:
            game_id (int, optional): Game ID filter
            season (int, optional): Season filter
            team (str, optional): Team name filter
            conference (str, optional): Conference abbreviation filter
            start_date (str or datetime, optional): Start date filter (ISO 8601 format)
            end_date (str or datetime, optional): End date filter (ISO 8601 format)
            season_type (str, optional): Season type filter ('regular', 'postseason', 'preseason')
            
        Returns:
            list: List of player statistics
        """
        params = {}
        
        if game_id:
            params['gameId'] = game_id
            
        if season:
            params['season'] = validate_season(season)
            
        if team:
            params['team'] = team
            
        if conference:
            params['conference'] = conference
            
        if start_date:
            params['startDateRange'] = validate_date(start_date)
            
        if end_date:
            params['endDateRange'] = validate_date(end_date)
            
        if season_type:
            if season_type not in [SeasonTypes.REGULAR, SeasonTypes.POSTSEASON, SeasonTypes.PRESEASON]:
                raise ValueError(f"Invalid season_type: {season_type}. Must be one of: 'regular', 'postseason', 'preseason'")
            params['seasonType'] = season_type
            
        return self._request(Endpoints.GAMES_PLAYERS, params) 