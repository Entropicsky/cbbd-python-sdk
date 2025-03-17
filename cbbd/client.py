"""
Client module for the CBBD Python SDK.

This module provides the main client class for interacting with
the College Basketball Data API.
"""

import os
import logging
from typing import Optional, Dict, Any, List, Callable
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Import base components without API modules that might not exist yet
from .exceptions import CBBDAuthError, CBBDRateLimitError, CBBDNotFoundError

# Add the transformers import
from .transformers import (
    BaseTransformer, 
    RosterTransformer, 
    TeamsTransformer, 
    GamesTransformer, 
    GameStatsTransformer,
    PlayerStatsTransformer,
    RankingsTransformer,
    RatingsTransformer,
    LinesTransformer,
    PlaysTransformer,
    DataFrameUtils
)

class Transformers:
    """
    Provides methods to transform API responses to pandas DataFrames.
    """
    
    def __init__(self, client):
        """
        Initialize the transformer with a reference to the client.
        
        Args:
            client: The CBBD client instance
        """
        self._client = client
        
    def roster_to_dataframe(self, roster_data: Any) -> 'pd.DataFrame':
        """
        Convert roster data to a pandas DataFrame.
        
        Args:
            roster_data: Roster data from the API
            
        Returns:
            pandas DataFrame with roster data
        """
        return RosterTransformer.to_dataframe(roster_data)
        
    def teams_to_dataframe(self, teams_data: Any) -> 'pd.DataFrame':
        """
        Convert teams data to a pandas DataFrame.
        
        Args:
            teams_data: Teams data from the API
            
        Returns:
            pandas DataFrame with teams data
        """
        return TeamsTransformer.to_dataframe(teams_data)
        
    def games_to_dataframe(self, games_data: Any) -> 'pd.DataFrame':
        """
        Convert games data to a pandas DataFrame.
        
        Args:
            games_data: Games data from the API
            
        Returns:
            pandas DataFrame with games data
        """
        return GamesTransformer.to_dataframe(games_data)
        
    def game_stats_to_dataframe(self, game_stats_data: Any) -> 'pd.DataFrame':
        """
        Convert game stats data to a pandas DataFrame.
        
        Args:
            game_stats_data: Game stats data from the API
            
        Returns:
            pandas DataFrame with game stats data
        """
        return GameStatsTransformer.boxscore_to_dataframe(game_stats_data)
        
    def player_stats_to_dataframe(self, player_stats_data: Any) -> 'pd.DataFrame':
        """
        Convert player stats data to a pandas DataFrame.
        
        Args:
            player_stats_data: Player stats data from the API
            
        Returns:
            pandas DataFrame with player stats data
        """
        return PlayerStatsTransformer.stats_to_dataframe(player_stats_data)
        
    def rankings_to_dataframe(self, rankings_data: Any) -> 'pd.DataFrame':
        """
        Convert rankings data to a pandas DataFrame.
        
        Args:
            rankings_data: Rankings data from the API
            
        Returns:
            pandas DataFrame with rankings data
        """
        return RankingsTransformer.to_dataframe(rankings_data)
        
    def ratings_to_dataframe(self, ratings_data: Any) -> 'pd.DataFrame':
        """
        Convert ratings data to a pandas DataFrame.
        
        Args:
            ratings_data: Ratings data from the API
            
        Returns:
            pandas DataFrame with ratings data
        """
        return RatingsTransformer.to_dataframe(ratings_data)
        
    def lines_to_dataframe(self, lines_data: Any) -> 'pd.DataFrame':
        """
        Convert betting lines data to a pandas DataFrame.
        
        Args:
            lines_data: Lines data from the API
            
        Returns:
            pandas DataFrame with betting lines data
        """
        return LinesTransformer.to_dataframe(lines_data)
        
    def plays_to_dataframe(self, plays_data: Any) -> 'pd.DataFrame':
        """
        Convert plays data to a pandas DataFrame.
        
        Args:
            plays_data: Plays data from the API
            
        Returns:
            pandas DataFrame with plays data
        """
        return PlaysTransformer.to_dataframe(plays_data)
        
    @property
    def utils(self) -> DataFrameUtils:
        """
        Get the DataFrame utilities.
        
        Returns:
            DataFrameUtils instance
        """
        return DataFrameUtils


class CBBDClient:
    """
    Main client for the College Basketball Data API.
    
    This client provides access to all API endpoints and features
    of the CBBD SDK.
    """
    
    def __init__(self, 
                api_key: Optional[str] = None,
                base_url: Optional[str] = None,
                use_cache: bool = True,
                cache_ttl: int = 3600,
                log_level: int = logging.INFO,
                log_format: Optional[str] = None,
                log_file: Optional[str] = None):
        """
        Initialize the CBBD client.
        
        Args:
            api_key: API key for authentication (optional if set in environment)
            base_url: Base URL for the API (optional, defaults to production)
            use_cache: Whether to use caching for API responses
            cache_ttl: Time to live for cache entries in seconds
            log_level: Logging level
            log_format: Custom log format
            log_file: Path to log file for logging
        """
        # Initialize logging
        self._setup_logging(log_level, log_format, log_file)
        
        # Get API key
        self.api_key = api_key or os.environ.get('CBBD_API_KEY') or os.environ.get('CFBD_API_KEY')
        if not self.api_key:
            load_dotenv()
            self.api_key = os.environ.get('CBBD_API_KEY') or os.environ.get('CFBD_API_KEY')
            
        if not self.api_key:
            logging.warning("No API key provided. Some API calls may fail.")
            
        # Set base URL
        self.base_url = base_url or "https://api.collegebasketballdata.com"
        
        # Create session with retry capabilities
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Wait to import API modules until needed to avoid circular imports
        self._imported_api_modules = False
        
        # Initialize transformers
        self.transformers = Transformers(self)
        
        # Cache settings
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl
        self.cache = {} if use_cache else None
        
        logging.info("CBBD client initialized successfully")
    
    def _import_api_modules(self):
        """Import API modules only when needed to avoid circular imports."""
        if self._imported_api_modules:
            return
            
        # Now import API modules
        try:
            from .api.conferences import ConferencesAPI
            from .api.teams import TeamsAPI
            from .api.games import GamesAPI
            from .api.players import PlayersAPI
            from .api.stats import StatsAPI
            from .api.rankings import RankingsAPI
            from .api.ratings import RatingsAPI
            from .api.venues import VenuesAPI
            from .api.plays import PlaysAPI
            from .api.lines import LinesAPI
            from .api.lineups import LineupsAPI
            from .api.draft import DraftAPI
            from .api.recruiting import RecruitingAPI
            from .api.substitutions import SubstitutionsAPI
            from .advanced import AdvancedAPI
            
            # Initialize API interfaces
            self.conferences = ConferencesAPI(self)
            self.teams = TeamsAPI(self)
            self.games = GamesAPI(self)
            self.players = PlayersAPI(self)
            self.stats = StatsAPI(self)
            self.rankings = RankingsAPI(self)
            self.ratings = RatingsAPI(self)
            self.venues = VenuesAPI(self)
            self.plays = PlaysAPI(self)
            self.lines = LinesAPI(self)
            self.lineups = LineupsAPI(self)
            self.draft = DraftAPI(self)
            self.recruiting = RecruitingAPI(self)
            self.substitutions = SubstitutionsAPI(self)
            
            # Initialize advanced API
            self.advanced = AdvancedAPI(self)
            
            self._imported_api_modules = True
        except ImportError as e:
            logging.error(f"Error importing API modules: {e}")
            raise
        
    def _setup_logging(self, 
                      log_level: int, 
                      log_format: Optional[str], 
                      log_file: Optional[str]) -> None:
        """
        Set up logging for the client.
        
        Args:
            log_level: Logging level
            log_format: Custom log format
            log_file: Path to log file
        """
        # Create logger
        logger = logging.getLogger('cbbd')
        logger.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            log_format or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Create file handler if log file specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
    def clear_cache(self) -> None:
        """Clear the API response cache."""
        if self.use_cache and self.cache:
            self.cache.clear()
            logging.info("Cache cleared")
            
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get statistics about the cache usage.
        
        Returns:
            Dictionary with cache statistics
        """
        if not self.use_cache or not self.cache:
            return {'enabled': False, 'entries': 0, 'size': 0}
            
        return {
            'enabled': True,
            'entries': len(self.cache),
            'size': sum(len(str(v)) for v in self.cache.values())
        }
        
    def __getattr__(self, name):
        """
        Lazily import API modules when an API attribute is first accessed.
        
        Args:
            name: Name of the attribute being accessed
            
        Returns:
            The requested attribute
            
        Raises:
            AttributeError: If the attribute doesn't exist
        """
        # Only try to import API modules for known API endpoint names
        api_endpoint_names = [
            'conferences', 'teams', 'games', 'players', 'stats', 
            'rankings', 'ratings', 'venues', 'plays', 'lines', 
            'lineups', 'draft', 'recruiting', 'substitutions', 'advanced'
        ]
        
        if name in api_endpoint_names and not self._imported_api_modules:
            self._import_api_modules()
            return getattr(self, name)
            
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'") 