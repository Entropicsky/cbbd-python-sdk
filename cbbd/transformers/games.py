"""
Games transformers for the CBBD SDK.

This module provides utilities for transforming games data from the CBBD API responses
into pandas DataFrames for easier analysis and visualization.
"""

import pandas as pd
from typing import Dict, List, Union, Any, Optional

from cbbd.transformers.base import BaseTransformer


class GamesTransformer(BaseTransformer):
    """
    Utility for transforming college basketball games data into DataFrames.
    
    This class provides methods for converting games data from the CBBD API
    into pandas DataFrames for easier analysis and visualization.
    """
    
    @staticmethod
    def to_dataframe(games_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert games data from the CBBD API into a pandas DataFrame.
        
        Args:
            games_data: Games data from the CBBD API. Can be a single game object,
                        a list of game objects, or a model object with get_raw_data method.
        
        Returns:
            pandas.DataFrame: DataFrame containing games data with standardized column names.
        """
        if games_data is None:
            return pd.DataFrame()
        
        # Extract raw data if this is a model object
        if hasattr(games_data, 'get_raw_data'):
            games_data = games_data.get_raw_data()
        
        # Handle empty data
        if not games_data:
            return pd.DataFrame()
        
        # Convert single game to list
        if isinstance(games_data, dict) and not any(isinstance(v, list) for v in games_data.values()):
            games_data = [games_data]
        
        # Create DataFrame
        df = pd.DataFrame(games_data)
        
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
        
        # Convert date columns
        date_cols = ['start_date', 'start_time_tbd']
        for col in date_cols:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except Exception:
                    pass  # Skip if conversion fails
        
        # Convert numeric columns
        numeric_cols = [
            'id', 'season', 'week', 'season_type', 
            'home_points', 'away_points', 'home_line_scores', 'away_line_scores',
            'home_win_prob', 'away_win_prob', 'excitement_index', 'attendance',
            'neutral_site', 'conference_game', 'tournament', 'overtime',
            'num_periods'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # If there are line score columns that contain lists, expand them
        if 'home_line_scores' in df.columns:
            GamesTransformer._expand_line_scores(df, 'home_line_scores', 'home_period')
            
        if 'away_line_scores' in df.columns:
            GamesTransformer._expand_line_scores(df, 'away_line_scores', 'away_period')
        
        # Add calculated columns
        if 'home_points' in df.columns and 'away_points' in df.columns:
            # Point differential (positive means home team won)
            df['point_differential'] = df['home_points'] - df['away_points']
            
            # Winner
            df['home_win'] = df['point_differential'] > 0
            df['away_win'] = df['point_differential'] < 0
            df['tie'] = df['point_differential'] == 0
            
            # Total points
            df['total_points'] = df['home_points'] + df['away_points']
        
        # Standardize column names (convert camelCase to snake_case)
        if any(c for c in df.columns if c[0].isupper() or any(char.isupper() for char in c[1:])):
            df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in df.columns]
        
        return df
    
    @staticmethod
    def boxscore_to_dataframe(boxscore_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert boxscore data from the CBBD API into a pandas DataFrame.
        
        Args:
            boxscore_data: Boxscore data from the CBBD API.
        
        Returns:
            pandas.DataFrame: DataFrame containing boxscore data with standardized column names.
        """
        if boxscore_data is None:
            return pd.DataFrame()
        
        # Extract raw data if this is a model object
        if hasattr(boxscore_data, 'get_raw_data'):
            boxscore_data = boxscore_data.get_raw_data()
        
        # Handle empty data
        if not boxscore_data:
            return pd.DataFrame()
        
        # For boxscores, we typically get a dict with teams and players stats
        # We'll return a dict of DataFrames for each component
        result_dfs = {}
        
        # Extract team stats
        if isinstance(boxscore_data, dict):
            # Handle team stats
            teams = []
            for team_type in ['home', 'away']:
                if f'{team_type}Team' in boxscore_data:
                    team_data = boxscore_data[f'{team_type}Team']
                    if team_data:
                        # Add the team type
                        team_data['team_type'] = team_type
                        teams.append(team_data)
            
            if teams:
                teams_df = pd.DataFrame(teams)
                
                # Clean NULL values
                for col in teams_df.columns:
                    teams_df[col] = teams_df[col].apply(BaseTransformer.clean_null_values)
                
                # Convert numeric columns - most boxscore stats are numeric
                for col in teams_df.columns:
                    if col not in ['team_type', 'team_id', 'team_name', 'conference']:
                        teams_df[col] = pd.to_numeric(teams_df[col], errors='coerce')
                
                # Standardize column names
                teams_df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in teams_df.columns]
                
                result_dfs['teams'] = teams_df
            
            # Handle player stats
            players = []
            for team_type in ['home', 'away']:
                if f'{team_type}Players' in boxscore_data:
                    player_list = boxscore_data[f'{team_type}Players']
                    if player_list:
                        for player in player_list:
                            # Add the team type
                            player['team_type'] = team_type
                            players.append(player)
            
            if players:
                players_df = pd.DataFrame(players)
                
                # Clean NULL values
                for col in players_df.columns:
                    players_df[col] = players_df[col].apply(BaseTransformer.clean_null_values)
                
                # Extract player info if nested
                if 'player' in players_df.columns and not pd.api.types.is_string_dtype(players_df['player']):
                    player_fields = ['id', 'name', 'position', 'jersey']
                    for field in player_fields:
                        players_df[f'player_{field}'] = players_df['player'].apply(
                            lambda x: BaseTransformer.extract_nested_value(x, field) if x is not None else None
                        )
                
                # Convert numeric columns - most boxscore stats are numeric
                for col in players_df.columns:
                    if col not in ['team_type', 'player_id', 'player', 'player_name', 'player_position']:
                        players_df[col] = pd.to_numeric(players_df[col], errors='coerce')
                
                # Standardize column names
                players_df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in players_df.columns]
                
                result_dfs['players'] = players_df
        
        # If we didn't extract any specialized data, just return a general DataFrame
        if not result_dfs and boxscore_data:
            df = pd.DataFrame([boxscore_data]) if isinstance(boxscore_data, dict) else pd.DataFrame(boxscore_data)
            
            # Clean NULL values
            for col in df.columns:
                df[col] = df[col].apply(BaseTransformer.clean_null_values)
            
            # Standardize column names
            df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in df.columns]
            
            return df
        
        return result_dfs
    
    @staticmethod
    def _expand_line_scores(df: pd.DataFrame, line_score_col: str, prefix: str) -> None:
        """
        Expand the line scores column into individual period columns.
        
        Args:
            df: DataFrame containing the line scores
            line_score_col: Column name containing the line scores list
            prefix: Prefix for the new period columns
        """
        # Skip if the column doesn't exist or is empty
        if line_score_col not in df.columns or df[line_score_col].isna().all():
            return
            
        # Find max number of periods across all games
        max_periods = 0
        for line_scores in df[line_score_col].dropna():
            if isinstance(line_scores, list):
                max_periods = max(max_periods, len(line_scores))
        
        # If no valid line scores, return
        if max_periods == 0:
            return
        
        # Create columns for each period
        for period in range(1, max_periods + 1):
            period_col = f'{prefix}_{period}'
            
            # Extract score for this period from the list
            df[period_col] = df[line_score_col].apply(
                lambda x: x[period-1] if isinstance(x, list) and len(x) >= period else None
            )
            
            # Convert to numeric
            df[period_col] = pd.to_numeric(df[period_col], errors='coerce')
