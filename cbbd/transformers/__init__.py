"""
Transformers for the CBBD SDK.

This module provides utilities for transforming data from the CBBD API responses
into pandas DataFrames for easier analysis and visualization.

Example:
    ```python
    from cbbd import CBBDClient
    from cbbd.transformers import TeamsTransformer

    client = CBBDClient(api_key="your_api_key")
    teams_data = client.teams.get_teams()
    
    # Convert to DataFrame
    transformer = TeamsTransformer()
    teams_df = transformer.to_dataframe(teams_data)
    ```
"""

from .base import BaseTransformer
from .games import GamesTransformer
from .teams import TeamsTransformer, RosterTransformer
from .players import PlayersTransformer
from .rankings import RankingsTransformer
from .ratings import RatingsTransformer
from .plays import PlaysTransformer
from .lines import LinesTransformer
from .venues import VenuesTransformer
from .utils import DataFrameUtils

# Define aliases for backward compatibility or convenience
GameStatsTransformer = GamesTransformer
PlayerStatsTransformer = PlayersTransformer

__all__ = [
    'BaseTransformer',
    'GamesTransformer',
    'GameStatsTransformer',
    'TeamsTransformer',
    'RosterTransformer',
    'PlayersTransformer',
    'PlayerStatsTransformer',
    'RankingsTransformer',
    'RatingsTransformer',
    'PlaysTransformer',
    'LinesTransformer',
    'VenuesTransformer',
    'DataFrameUtils',
] 