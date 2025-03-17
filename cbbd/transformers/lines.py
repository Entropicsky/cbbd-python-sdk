"""
Lines transformers for the CBBD SDK.

This module provides utilities for transforming betting lines data from the CBBD API responses
into pandas DataFrames for easier analysis and visualization.
"""

import pandas as pd
from typing import Dict, List, Union, Any, Optional

from cbbd.transformers.base import BaseTransformer


class LinesTransformer(BaseTransformer):
    """
    Utility for transforming college basketball betting lines data into DataFrames.
    
    This class provides methods for converting betting lines data from the CBBD API
    into pandas DataFrames for easier analysis and visualization.
    """
    
    @staticmethod
    def to_dataframe(lines_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert betting lines data from the CBBD API into a pandas DataFrame.
        
        Args:
            lines_data: Betting lines data from the CBBD API. Can be a single line object,
                        a list of line objects, or a model object with get_raw_data method.
        
        Returns:
            pandas.DataFrame: DataFrame containing betting lines data with standardized column names.
        """
        if lines_data is None:
            return pd.DataFrame()
        
        # Extract raw data if this is a model object
        if hasattr(lines_data, 'get_raw_data'):
            lines_data = lines_data.get_raw_data()
        
        # Handle empty data
        if not lines_data:
            return pd.DataFrame()
        
        # Convert single line to list
        if isinstance(lines_data, dict) and not any(isinstance(v, list) for v in lines_data.values()):
            lines_data = [lines_data]
        
        # Create DataFrame
        df = pd.DataFrame(lines_data)
        
        # Clean NULL values
        for col in df.columns:
            df[col] = df[col].apply(BaseTransformer.clean_null_values)
        
        # Extract team info if nested
        if 'home_team' in df.columns and not pd.api.types.is_string_dtype(df['home_team']):
            team_fields = ['id', 'name', 'conference', 'mascot', 'abbreviation']
            for field in team_fields:
                df[f'home_team_{field}'] = df['home_team'].apply(
                    lambda x: BaseTransformer.extract_nested_value(x, field) if x is not None else None
                )
            
        if 'away_team' in df.columns and not pd.api.types.is_string_dtype(df['away_team']):
            team_fields = ['id', 'name', 'conference', 'mascot', 'abbreviation']
            for field in team_fields:
                df[f'away_team_{field}'] = df['away_team'].apply(
                    lambda x: BaseTransformer.extract_nested_value(x, field) if x is not None else None
                )
        
        # Convert numeric columns
        numeric_cols = [
            'id', 'season', 'week', 'home_score', 'away_score',
            'spread', 'over_under', 'home_moneyline', 'away_moneyline',
            'formatted_spread', 'formatted_over_under'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert date columns
        date_cols = ['start_date']
        for col in date_cols:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except Exception:
                    pass  # Skip if conversion fails
        
        # Add calculated columns for analysis
        if 'home_score' in df.columns and 'away_score' in df.columns:
            # Only calculate if the game has been played
            score_mask = ~df['home_score'].isna() & ~df['away_score'].isna()
            
            # Point differential (positive means home team won)
            df.loc[score_mask, 'point_differential'] = df.loc[score_mask, 'home_score'] - df.loc[score_mask, 'away_score']
            
            # Total points
            df.loc[score_mask, 'total_points'] = df.loc[score_mask, 'home_score'] + df.loc[score_mask, 'away_score']
            
            # Bet outcomes
            if 'spread' in df.columns:
                # Spread bet outcome (1 = home team covers, 0 = push, -1 = away team covers)
                df.loc[score_mask, 'spread_outcome'] = (df.loc[score_mask, 'point_differential'] + df.loc[score_mask, 'spread']).apply(
                    lambda x: 1 if x > 0 else (0 if x == 0 else -1)
                )
            
            if 'over_under' in df.columns:
                # Over/under bet outcome (1 = over, 0 = push, -1 = under)
                df.loc[score_mask, 'over_under_outcome'] = (df.loc[score_mask, 'total_points'] - df.loc[score_mask, 'over_under']).apply(
                    lambda x: 1 if x > 0 else (0 if x == 0 else -1)
                )
        
        # Standardize column names (convert camelCase to snake_case)
        if any(c for c in df.columns if c[0].isupper() or any(char.isupper() for char in c[1:])):
            df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in df.columns]
        
        return df
    
    @staticmethod
    def provider_lines_to_dataframe(lines_data: Union[Dict, List, Any, None], provider: Optional[str] = None) -> pd.DataFrame:
        """
        Convert betting lines data from a specific provider into a pandas DataFrame.
        
        Args:
            lines_data: Betting lines data from the CBBD API.
            provider: Name of the betting provider to filter by (e.g., 'consensus', 'draftkings').
                     If None, all providers will be included.
        
        Returns:
            pandas.DataFrame: DataFrame containing betting lines data for the specified provider.
        """
        df = LinesTransformer.to_dataframe(lines_data)
        
        if df.empty:
            return df
        
        # Filter by provider if specified
        if provider and 'provider' in df.columns:
            # Case-insensitive comparison
            df = df[df['provider'].str.lower() == provider.lower()].copy()
        
        return df
    
    @staticmethod
    def lines_trends_to_dataframe(lines_data: Union[Dict, List, Any, None], 
                                 team: Optional[str] = None) -> pd.DataFrame:
        """
        Convert betting lines data into a format suitable for trend analysis.
        
        This method organizes lines data to show trends over time for a team.
        
        Args:
            lines_data: Betting lines data from the CBBD API.
            team: Team name to filter lines for.
        
        Returns:
            pandas.DataFrame: DataFrame organized to show betting lines trends.
        """
        df = LinesTransformer.to_dataframe(lines_data)
        
        if df.empty:
            return df
        
        # Filter by team if specified
        if team:
            team_columns = ['home_team_name', 'away_team_name', 'home_team', 'away_team']
            
            # Find which column has the team name
            for col in team_columns:
                if col in df.columns:
                    if df[col].dtype == 'object':
                        # Add a flag to indicate if this team is home or away
                        if 'home' in col:
                            mask = df[col] == team
                            df.loc[mask, 'is_home'] = True
                        else:
                            mask = df[col] == team
                            df.loc[mask, 'is_home'] = False
                        
                        df = df[mask].copy()
                        break
        
        # Ensure we have the necessary columns
        required_cols = ['start_date', 'spread', 'over_under', 'provider']
        
        # Add opponent column
        if 'is_home' in df.columns:
            df['opponent'] = df.apply(
                lambda row: row['away_team_name'] if row['is_home'] else row['home_team_name'],
                axis=1
            )
            required_cols.append('opponent')
        
        # Check if we have all required columns
        if not all(col in df.columns for col in required_cols):
            # If not, return what we have
            return df
        
        # Sort by date
        if 'start_date' in df.columns:
            df = df.sort_values(by='start_date')
        
        return df
