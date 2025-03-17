"""
Players transformers for the CBBD SDK.

This module provides utilities for transforming player data from the CBBD API responses
into pandas DataFrames for easier analysis and visualization.
"""

import pandas as pd
from typing import Dict, List, Union, Optional, Any
import logging

from cbbd.transformers.base import BaseTransformer
from ..models.players import Player

logger = logging.getLogger(__name__)

class PlayersTransformer(BaseTransformer):
    """
    Utility for transforming college basketball player data into DataFrames.
    
    This class provides methods for converting player statistics and information
    from the CBBD API into pandas DataFrames for easier analysis and visualization.
    """
    
    def to_dataframe(self, data: Any) -> pd.DataFrame:
        """
        Convert player data to a pandas DataFrame.
        
        Args:
            data: Player data to convert, can be a list of Player objects or raw dictionaries.
            
        Returns:
            A pandas DataFrame containing the player data.
        """
        if not data:
            logger.warning("No data provided to transform")
            return pd.DataFrame()
            
        try:
            players_data = []
            
            # Process raw API responses or Player objects
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, Player):
                        players_data.append(self._player_to_dict(item))
                    elif isinstance(item, dict):
                        players_data.append(item)
                    else:
                        logger.warning(f"Unexpected item type in player data: {type(item)}")
            elif isinstance(data, Player):
                players_data.append(self._player_to_dict(data))
            elif hasattr(data, 'players') and data.players:  # For team roster objects
                for player in data.players:
                    if isinstance(player, Player):
                        players_data.append(self._player_to_dict(player))
                    elif isinstance(player, dict):
                        players_data.append(player)
                    else:
                        logger.warning(f"Unexpected player type in roster: {type(player)}")
            else:
                logger.warning(f"Unsupported data type for player transformation: {type(data)}")
                return pd.DataFrame()
                
            if not players_data:
                logger.warning("No valid player data found to transform")
                return pd.DataFrame()
                
            # Convert to DataFrame
            df = pd.DataFrame(players_data)
            
            # Process hometown columns if present
            if 'hometown' in df.columns:
                df = self._process_hometown_columns(df)
                
            # Convert date columns if present
            if 'date_of_birth' in df.columns:
                df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
                
            return df
            
        except Exception as e:
            logger.error(f"Error transforming player data to DataFrame: {e}")
            return pd.DataFrame()
            
    def _player_to_dict(self, player: Player) -> Dict:
        """
        Convert a Player object to a dictionary.
        
        Args:
            player: The Player object to convert.
            
        Returns:
            A dictionary representation of the player.
        """
        if not player:
            return {}
            
        player_dict = {
            'id': player.id,
            'source_id': player.source_id,
            'name': player.name,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'jersey': player.jersey,
            'position': player.position,
            'height': player.height,
            'weight': player.weight,
            'date_of_birth': player.date_of_birth,
            'start_season': player.start_season,
            'end_season': player.end_season,
            'team': player.team,
            'conference': player.conference
        }
        
        # Add hometown data if available
        if player.hometown:
            player_dict['city'] = player.hometown.city
            player_dict['state'] = player.hometown.state
            player_dict['country'] = player.hometown.country
            player_dict['latitude'] = player.hometown.latitude
            player_dict['longitude'] = player.hometown.longitude
            
        return player_dict
        
    def _process_hometown_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process the hometown column in a DataFrame to extract city, state, etc.
        
        Args:
            df: The DataFrame to process.
            
        Returns:
            The processed DataFrame.
        """
        if 'hometown' not in df.columns:
            return df
            
        try:
            # Create new columns for hometown data if not already present
            if isinstance(df['hometown'].iloc[0], dict):
                for field in ['city', 'state', 'country', 'latitude', 'longitude']:
                    if field not in df.columns:
                        df[field] = df['hometown'].apply(lambda x: x.get(field) if isinstance(x, dict) else None)
                        
            # Drop the original hometown column
            df = df.drop(columns=['hometown'])
            
        except Exception as e:
            logger.error(f"Error processing hometown columns: {e}")
            
        return df
    
    @staticmethod
    def stats_to_dataframe(stats_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert player statistics data from the CBBD API into a pandas DataFrame.
        
        Args:
            stats_data: Player statistics data from the CBBD API.
        
        Returns:
            pandas.DataFrame: DataFrame containing player statistics with standardized column names.
        """
        if stats_data is None:
            return pd.DataFrame()
        
        # Extract raw data if this is a model object
        if hasattr(stats_data, 'get_raw_data'):
            stats_data = stats_data.get_raw_data()
        
        # Handle empty data
        if not stats_data:
            return pd.DataFrame()
        
        # Convert single stats object to list
        if isinstance(stats_data, dict) and not any(isinstance(v, list) for v in stats_data.values()):
            stats_data = [stats_data]
        
        # Create DataFrame
        df = pd.DataFrame(stats_data)
        
        # Clean NULL values
        for col in df.columns:
            df[col] = df[col].apply(BaseTransformer.clean_null_values)
        
        # Extract player and team info if nested
        if 'player' in df.columns and not pd.api.types.is_string_dtype(df['player']):
            player_fields = ['id', 'name', 'position', 'jersey']
            for field in player_fields:
                df[f'player_{field}'] = df['player'].apply(
                    lambda x: BaseTransformer.extract_nested_value(x, field) if x is not None else None
                )
            
        if 'team' in df.columns and not pd.api.types.is_string_dtype(df['team']):
            team_fields = ['id', 'name', 'conference']
            for field in team_fields:
                df[f'team_{field}'] = df['team'].apply(
                    lambda x: BaseTransformer.extract_nested_value(x, field) if x is not None else None
                )
        
        # Convert numeric columns
        numeric_cols = [
            'season', 'jersey', 'games', 'minutes', 
            'fieldGoalsMade', 'fieldGoalsAttempted', 'fieldGoalPercentage',
            'twoPointMade', 'twoPointAttempted', 'twoPointPercentage',
            'threePointMade', 'threePointAttempted', 'threePointPercentage',
            'freeThrowsMade', 'freeThrowsAttempted', 'freeThrowPercentage',
            'offensiveRebounds', 'defensiveRebounds', 'rebounds',
            'assists', 'steals', 'blocks', 'turnovers', 'fouls', 'points'
        ]
        
        # Add advanced stats if they exist
        advanced_cols = [
            'offensiveRating', 'defensiveRating', 'netRating', 
            'assistPercentage', 'blockPercentage', 'stealPercentage',
            'effectiveFieldGoalPercentage', 'trueShootingPercentage',
            'usageRate', 'playerEfficiencyRating', 'winShares'
        ]
        numeric_cols.extend(advanced_cols)
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Calculate per game stats if not already present
        per_game_stats = {
            'pointsPerGame': 'points',
            'reboundsPerGame': 'rebounds',
            'assistsPerGame': 'assists',
            'stealsPerGame': 'steals',
            'blocksPerGame': 'blocks',
            'turnoversPerGame': 'turnovers'
        }
        
        for new_col, base_col in per_game_stats.items():
            if new_col not in df.columns and base_col in df.columns and 'games' in df.columns:
                df[new_col] = df[base_col] / df['games']
        
        # Standardize column names (convert camelCase to snake_case)
        df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in df.columns]
        
        return df
    
    @staticmethod
    def _build_hometown_string(city: Optional[str], state: Optional[str], country: Optional[str]) -> Optional[str]:
        """
        Build a formatted hometown string from city, state, and country components.
        
        Args:
            city: City name or None
            state: State abbreviation or None
            country: Country name or None
            
        Returns:
            str: Formatted hometown string or None if all components are None
        """
        components = []
        
        if city:
            components.append(city)
            
        if state:
            components.append(state)
        
        # Only add country if it's not USA or if there's no state
        if country and (country != "USA" or not state):
            components.append(country)
            
        if not components:
            return None
            
        return ", ".join(components)
