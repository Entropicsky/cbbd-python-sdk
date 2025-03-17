"""
Rankings transformers for the CBBD SDK.

This module provides utilities for transforming rankings data from the CBBD API responses
into pandas DataFrames for easier analysis and visualization.
"""

import pandas as pd
from typing import Dict, List, Union, Any, Optional

from cbbd.transformers.base import BaseTransformer


class RankingsTransformer(BaseTransformer):
    """
    Utility for transforming college basketball rankings data into DataFrames.
    
    This class provides methods for converting rankings data from the CBBD API
    into pandas DataFrames for easier analysis and visualization.
    """
    
    @staticmethod
    def to_dataframe(rankings_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert rankings data from the CBBD API into a pandas DataFrame.
        
        Args:
            rankings_data: Rankings data from the CBBD API. Can be a single rankings object,
                           a list of rankings objects, or a model object with get_raw_data method.
        
        Returns:
            pandas.DataFrame: DataFrame containing rankings data with standardized column names.
        """
        if rankings_data is None:
            return pd.DataFrame()
        
        # Extract raw data if this is a model object
        if hasattr(rankings_data, 'get_raw_data'):
            rankings_data = rankings_data.get_raw_data()
        
        # Handle empty data
        if not rankings_data:
            return pd.DataFrame()
        
        # Rankings data can be nested with polls and teams
        # First we'll handle the case where it's a list of polls
        if isinstance(rankings_data, list) and all(isinstance(item.get('polls'), list) for item in rankings_data if isinstance(item, dict)):
            # Flatten the rankings data
            flattened_rankings = []
            
            for ranking in rankings_data:
                season = ranking.get('season')
                
                for poll in ranking.get('polls', []):
                    poll_name = poll.get('poll')
                    poll_ranks = poll.get('ranks', [])
                    
                    for rank in poll_ranks:
                        record = {
                            'season': season,
                            'poll': poll_name,
                            'rank': rank.get('rank'),
                            'school': rank.get('school'),
                            'conference': rank.get('conference'),
                            'first_place_votes': rank.get('firstPlaceVotes'),
                            'points': rank.get('points')
                        }
                        
                        # Add team info if available
                        if 'team' in rank and isinstance(rank['team'], dict):
                            for team_field, team_value in rank['team'].items():
                                record[f'team_{team_field}'] = team_value
                        
                        flattened_rankings.append(record)
            
            # Create DataFrame from flattened data
            df = pd.DataFrame(flattened_rankings)
        
        # Handle case where it's already a flat structure
        elif isinstance(rankings_data, list):
            # Create DataFrame
            df = pd.DataFrame(rankings_data)
        else:
            # Handle single object case
            df = pd.DataFrame([rankings_data])
        
        # Clean NULL values
        for col in df.columns:
            df[col] = df[col].apply(BaseTransformer.clean_null_values)
        
        # Convert numeric columns
        numeric_cols = ['season', 'week', 'rank', 'first_place_votes', 'points']
        camel_case_numeric_cols = ['season', 'week', 'rank', 'firstPlaceVotes', 'points']
        
        # Check which naming convention is used
        for col_list in [numeric_cols, camel_case_numeric_cols]:
            for col in col_list:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Standardize column names (convert camelCase to snake_case)
        if any(c for c in df.columns if c[0].isupper() or any(char.isupper() for char in c[1:])):
            df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in df.columns]
        
        return df
    
    @staticmethod
    def poll_rankings_to_dataframe(rankings_data: Union[Dict, List, Any, None], poll: Optional[str] = None) -> pd.DataFrame:
        """
        Convert poll-specific rankings data into a pandas DataFrame.
        
        Args:
            rankings_data: Rankings data from the CBBD API.
            poll: Name of the poll to filter by (e.g., 'AP Top 25', 'Coaches Poll')
                  If None, all polls will be included.
        
        Returns:
            pandas.DataFrame: DataFrame containing poll rankings data.
        """
        df = RankingsTransformer.to_dataframe(rankings_data)
        
        if df.empty:
            return df
        
        # Filter by poll if specified
        if poll and 'poll' in df.columns:
            df = df[df['poll'] == poll].copy()
        
        return df
    
    @staticmethod
    def ranking_trends_to_dataframe(rankings_data: Union[Dict, List, Any, None], 
                                   team: Optional[str] = None,
                                   poll: Optional[str] = None) -> pd.DataFrame:
        """
        Convert rankings data into a format suitable for trend analysis.
        
        This method organizes rankings data by week to show trends over time.
        
        Args:
            rankings_data: Rankings data from the CBBD API.
            team: Team name to filter rankings for.
            poll: Poll name to filter rankings for.
        
        Returns:
            pandas.DataFrame: DataFrame organized by week showing ranking trends.
        """
        df = RankingsTransformer.to_dataframe(rankings_data)
        
        if df.empty:
            return df
        
        # Filter by team if specified
        if team:
            team_col = 'school' if 'school' in df.columns else 'team_name' if 'team_name' in df.columns else None
            if team_col:
                df = df[df[team_col] == team].copy()
        
        # Filter by poll if specified
        if poll and 'poll' in df.columns:
            df = df[df['poll'] == poll].copy()
        
        # Ensure we have the necessary columns
        required_cols = ['season', 'week', 'rank', 'poll']
        school_col = 'school' if 'school' in df.columns else 'team_name' if 'team_name' in df.columns else None
        
        if school_col:
            required_cols.append(school_col)
        
        # Check if we have all required columns
        if not all(col in df.columns for col in required_cols):
            # If not, return what we have
            return df
        
        # Sort by season, week, and poll
        sort_cols = ['season', 'week', 'poll']
        if school_col:
            sort_cols.append(school_col)
        
        df = df.sort_values(by=sort_cols)
        
        return df
