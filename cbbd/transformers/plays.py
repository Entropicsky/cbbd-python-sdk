"""
Plays transformers for the CBBD SDK.

This module provides utilities for transforming play-by-play data from the CBBD API responses
into pandas DataFrames for easier analysis and visualization.
"""

import pandas as pd
from typing import Dict, List, Union, Any, Optional

from cbbd.transformers.base import BaseTransformer


class PlaysTransformer(BaseTransformer):
    """
    Utility for transforming college basketball play-by-play data into DataFrames.
    
    This class provides methods for converting play-by-play data from the CBBD API
    into pandas DataFrames for easier analysis and visualization.
    """
    
    @staticmethod
    def to_dataframe(plays_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert play-by-play data from the CBBD API into a pandas DataFrame.
        
        Args:
            plays_data: Play-by-play data from the CBBD API. Can be a single play object,
                        a list of play objects, or a model object with get_raw_data method.
        
        Returns:
            pandas.DataFrame: DataFrame containing play-by-play data with standardized column names.
        """
        if plays_data is None:
            return pd.DataFrame()
        
        # Extract raw data if this is a model object
        if hasattr(plays_data, 'get_raw_data'):
            plays_data = plays_data.get_raw_data()
        
        # Handle empty data
        if not plays_data:
            return pd.DataFrame()
        
        # Play-by-play data is often structured with a wrapper containing game metadata
        # and a list of plays
        if isinstance(plays_data, dict) and 'plays' in plays_data:
            # Extract game metadata
            game_data = {k: v for k, v in plays_data.items() if k != 'plays'}
            plays = plays_data['plays']
            
            # If the plays list is empty, return an empty DataFrame
            if not plays:
                return pd.DataFrame()
            
            # Create DataFrame from plays list
            df = pd.DataFrame(plays)
            
            # Add game metadata as columns to each play
            for key, value in game_data.items():
                df[key] = value
        
        # Handle case where it's a flat list of plays
        elif isinstance(plays_data, list):
            # Create DataFrame
            df = pd.DataFrame(plays_data)
        
        # Handle single play object case
        else:
            # Create DataFrame with a single row
            df = pd.DataFrame([plays_data])
        
        # Clean NULL values
        for col in df.columns:
            df[col] = df[col].apply(BaseTransformer.clean_null_values)
        
        # Extract team info if nested
        for team_type in ['home', 'away']:
            team_col = f'{team_type}_team'
            if team_col in df.columns and not pd.api.types.is_string_dtype(df[team_col]):
                team_fields = ['id', 'name', 'conference', 'mascot', 'abbreviation']
                for field in team_fields:
                    df[f'{team_col}_{field}'] = df[team_col].apply(
                        lambda x: BaseTransformer.extract_nested_value(x, field) if x is not None else None
                    )
        
        # Convert date/time columns
        time_cols = ['clock']
        for col in time_cols:
            if col in df.columns and df[col].dtype == 'object':
                # Handle game clock format (MM:SS)
                try:
                    # Extract minutes and seconds
                    df[f'{col}_seconds'] = df[col].str.split(':').apply(
                        lambda x: int(x[0]) * 60 + int(x[1]) if isinstance(x, list) and len(x) == 2 else None
                    )
                except Exception:
                    pass
        
        # Convert numeric columns
        numeric_cols = [
            'id', 'period', 'period_number', 'play_number', 'sequence_number',
            'home_score', 'away_score', 'score_value', 'scoring_play',
            'coordinate_x', 'coordinate_y'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Add calculated columns for analysis
        if 'home_score' in df.columns and 'away_score' in df.columns:
            # Point differential at this moment (positive means home team is ahead)
            df['score_differential'] = df['home_score'] - df['away_score']
            
            # Total score at this moment
            df['total_score'] = df['home_score'] + df['away_score']
            
            # Score change from previous play
            df['score_change'] = df['total_score'].diff()
        
        # Standardize column names (convert camelCase to snake_case)
        if any(c for c in df.columns if c[0].isupper() or any(char.isupper() for char in c[1:])):
            df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in df.columns]
        
        return df
    
    @staticmethod
    def scoring_plays_to_dataframe(plays_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert play-by-play data into a DataFrame containing only scoring plays.
        
        Args:
            plays_data: Play-by-play data from the CBBD API.
        
        Returns:
            pandas.DataFrame: DataFrame containing only scoring plays.
        """
        df = PlaysTransformer.to_dataframe(plays_data)
        
        if df.empty:
            return df
        
        # Filter to scoring plays
        if 'scoring_play' in df.columns:
            df = df[df['scoring_play'] == True].copy()
        elif 'score_value' in df.columns:
            df = df[df['score_value'] > 0].copy()
        else:
            # If neither column exists, try to infer scoring plays from score change
            if 'score_change' in df.columns:
                df = df[df['score_change'] > 0].copy()
        
        return df
    
    @staticmethod
    def play_types_to_dataframe(plays_data: Union[Dict, List, Any, None], 
                              play_type: Optional[str] = None,
                              team: Optional[str] = None) -> pd.DataFrame:
        """
        Convert play-by-play data into a DataFrame filtered by play type and/or team.
        
        Args:
            plays_data: Play-by-play data from the CBBD API.
            play_type: Type of play to filter for (e.g., 'made3', 'miss', 'turnover', 'foul').
            team: Team name to filter plays for.
        
        Returns:
            pandas.DataFrame: DataFrame containing plays of the specified type and/or team.
        """
        df = PlaysTransformer.to_dataframe(plays_data)
        
        if df.empty:
            return df
        
        # Filter by play type if specified
        if play_type:
            play_type_col = 'type' if 'type' in df.columns else 'play_type' if 'play_type' in df.columns else None
            if play_type_col:
                df = df[df[play_type_col].str.lower() == play_type.lower()].copy()
        
        # Filter by team if specified
        if team:
            team_cols = [
                'team', 'team_name', 'home_team_name', 'away_team_name', 
                'home_team', 'away_team'
            ]
            
            # Find which column has the team name
            team_found = False
            for col in team_cols:
                if col in df.columns and df[col].dtype == 'object':
                    mask = df[col].str.lower() == team.lower()
                    if mask.any():
                        df = df[mask].copy()
                        team_found = True
                        break
            
            # If team wasn't found in any column
            if not team_found:
                return pd.DataFrame()
        
        return df
    
    @staticmethod
    def game_flow_to_dataframe(plays_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert play-by-play data into a game flow format showing score progression.
        
        Args:
            plays_data: Play-by-play data from the CBBD API.
        
        Returns:
            pandas.DataFrame: DataFrame organized to show game flow with score progressions.
        """
        df = PlaysTransformer.to_dataframe(plays_data)
        
        if df.empty:
            return df
        
        # Ensure we have the necessary columns
        required_cols = ['period', 'clock', 'home_score', 'away_score']
        if not all(col in df.columns for col in required_cols):
            return df
        
        # Add period time in seconds from the start of the game
        if 'period' in df.columns and 'clock_seconds' in df.columns:
            # Assuming college basketball has 20-minute periods
            period_length_seconds = 20 * 60
            
            df['game_seconds'] = (df['period'] - 1) * period_length_seconds + (period_length_seconds - df['clock_seconds'])
            
            # Sort by game time (period and clock)
            df = df.sort_values(by=['game_seconds'])
        
        return df
