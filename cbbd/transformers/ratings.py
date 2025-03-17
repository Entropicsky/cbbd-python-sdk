"""
Ratings transformers for the CBBD SDK.

This module provides utilities for transforming ratings data from the CBBD API responses
into pandas DataFrames for easier analysis and visualization.
"""

import pandas as pd
from typing import Dict, List, Union, Any, Optional

from cbbd.transformers.base import BaseTransformer


class RatingsTransformer(BaseTransformer):
    """
    Utility for transforming college basketball ratings data into DataFrames.
    
    This class provides methods for converting ratings data from the CBBD API
    into pandas DataFrames for easier analysis and visualization.
    """
    
    @staticmethod
    def to_dataframe(ratings_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert ratings data from the CBBD API into a pandas DataFrame.
        
        Args:
            ratings_data: Ratings data from the CBBD API. Can be a single ratings object,
                           a list of ratings objects, or a model object with get_raw_data method.
        
        Returns:
            pandas.DataFrame: DataFrame containing ratings data with standardized column names.
        """
        if ratings_data is None:
            return pd.DataFrame()
        
        # Extract raw data if this is a model object
        if hasattr(ratings_data, 'get_raw_data'):
            ratings_data = ratings_data.get_raw_data()
        
        # Handle empty data
        if not ratings_data:
            return pd.DataFrame()
        
        # Ratings data may have multiple rating systems
        if isinstance(ratings_data, list) and all(isinstance(item, dict) and 'teams' in item for item in ratings_data):
            # This is a list of rating systems with teams
            flattened_ratings = []
            
            for rating_system in ratings_data:
                system_name = rating_system.get('name')
                
                for team in rating_system.get('teams', []):
                    record = {
                        'rating_system': system_name,
                        'rank': team.get('rank'),
                        'school': team.get('school'),
                        'conference': team.get('conference'),
                        'rating': team.get('rating')
                    }
                    
                    # Add season if available
                    if 'season' in rating_system:
                        record['season'] = rating_system['season']
                    
                    # Add team info if available
                    if 'team' in team and isinstance(team['team'], dict):
                        for team_field, team_value in team['team'].items():
                            record[f'team_{team_field}'] = team_value
                    
                    flattened_ratings.append(record)
            
            # Create DataFrame from flattened data
            df = pd.DataFrame(flattened_ratings)
        
        # Handle case where it's already a flat structure
        elif isinstance(ratings_data, list):
            # Create DataFrame
            df = pd.DataFrame(ratings_data)
        else:
            # Handle single object case
            df = pd.DataFrame([ratings_data])
        
        # Clean NULL values
        for col in df.columns:
            df[col] = df[col].apply(BaseTransformer.clean_null_values)
        
        # Convert numeric columns
        numeric_cols = ['rank', 'rating', 'season', 'wins', 'losses', 'sos']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Standardize column names (convert camelCase to snake_case)
        if any(c for c in df.columns if c[0].isupper() or any(char.isupper() for char in c[1:])):
            df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in df.columns]
        
        return df
    
    @staticmethod
    def sp_ratings_to_dataframe(ratings_data: Union[Dict, List, Any, None]) -> pd.DataFrame:
        """
        Convert SP+ ratings data from the CBBD API into a pandas DataFrame.
        
        Args:
            ratings_data: SP+ ratings data from the CBBD API.
        
        Returns:
            pandas.DataFrame: DataFrame containing SP+ ratings data.
        """
        df = RatingsTransformer.to_dataframe(ratings_data)
        
        if df.empty:
            return df
        
        # Filter to SP+ ratings if rating_system column exists
        if 'rating_system' in df.columns:
            sp_keywords = ['sp+', 'sp', 'sp plus']
            mask = df['rating_system'].str.lower().isin(sp_keywords) if df['rating_system'].dtype == 'object' else False
            df = df[mask].copy()
        
        # Additional processing specific to SP+ ratings
        numeric_cols = ['offense', 'defense', 'special_teams']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    @staticmethod
    def compare_ratings_to_dataframe(ratings_data: Union[Dict, List, Any, None], 
                                    team: Optional[str] = None) -> pd.DataFrame:
        """
        Convert ratings data into a format suitable for comparing different rating systems.
        
        This method organizes ratings data by rating system to compare ratings across systems.
        
        Args:
            ratings_data: Ratings data from the CBBD API.
            team: Team name to filter ratings for.
        
        Returns:
            pandas.DataFrame: DataFrame organized by rating system for comparison.
        """
        df = RatingsTransformer.to_dataframe(ratings_data)
        
        if df.empty:
            return df
        
        # Filter by team if specified
        if team:
            team_col = 'school' if 'school' in df.columns else 'team_name' if 'team_name' in df.columns else None
            if team_col:
                df = df[df[team_col] == team].copy()
        
        # Ensure we have the necessary columns
        required_cols = ['rating_system', 'rank', 'rating']
        school_col = 'school' if 'school' in df.columns else 'team_name' if 'team_name' in df.columns else None
        
        if school_col:
            required_cols.append(school_col)
        
        # Check if we have all required columns
        if not all(col in df.columns for col in required_cols):
            # If not, return what we have
            return df
        
        # Sort by rating system and rank
        sort_cols = ['rating_system', 'rank']
        df = df.sort_values(by=sort_cols)
        
        return df
