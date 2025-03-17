"""
Utility functions for data transformations.

This module provides helper functions for working with transformed data,
including visualization preparation and common data operations.
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Tuple, Union, Callable

class DataFrameUtils:
    """Utilities for working with DataFrames in the context of basketball data."""
    
    @staticmethod
    def make_visualization_ready(df: pd.DataFrame, 
                                numeric_columns: Optional[List[str]] = None,
                                categorical_columns: Optional[List[str]] = None,
                                date_columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Prepare a DataFrame for visualization by ensuring proper data types.
        
        Args:
            df: Input DataFrame
            numeric_columns: Columns to convert to numeric
            categorical_columns: Columns to convert to categorical
            date_columns: Columns to convert to datetime
            
        Returns:
            Prepared DataFrame
        """
        result = df.copy()
        
        # Handle numeric columns
        if numeric_columns:
            for col in numeric_columns:
                if col in result.columns:
                    # Handle 'NULL' string values
                    result[col] = result[col].replace('NULL', np.nan)
                    result[col] = pd.to_numeric(result[col], errors='coerce')
        
        # Handle categorical columns
        if categorical_columns:
            for col in categorical_columns:
                if col in result.columns:
                    # Remove NULL values before conversion
                    result[col] = result[col].replace('NULL', np.nan)
                    # Convert to category
                    result[col] = result[col].astype('category')
        
        # Handle date columns
        if date_columns:
            for col in date_columns:
                if col in result.columns:
                    result[col] = pd.to_datetime(result[col], errors='coerce')
        
        return result
    
    @staticmethod
    def add_calculated_columns(df: pd.DataFrame, 
                              calculations: Dict[str, Callable[[pd.DataFrame], pd.Series]]) -> pd.DataFrame:
        """
        Add calculated columns to a DataFrame based on provided functions.
        
        Args:
            df: Input DataFrame
            calculations: Dictionary mapping new column names to functions that calculate values
            
        Returns:
            DataFrame with additional calculated columns
        """
        result = df.copy()
        
        for col_name, calc_func in calculations.items():
            try:
                result[col_name] = calc_func(result)
            except Exception as e:
                # Log the error but continue with other calculations
                print(f"Error calculating column {col_name}: {e}")
                
        return result
    
    @staticmethod
    def filter_season(df: pd.DataFrame, 
                     season: int, 
                     season_column: str = 'season') -> pd.DataFrame:
        """
        Filter a DataFrame to a specific season.
        
        Args:
            df: Input DataFrame
            season: Season to filter to
            season_column: Name of the column containing season values
            
        Returns:
            Filtered DataFrame
        """
        if season_column in df.columns:
            return df[df[season_column] == season]
        return df
    
    @staticmethod
    def filter_team(df: pd.DataFrame, 
                   team: str, 
                   team_column: str = 'team') -> pd.DataFrame:
        """
        Filter a DataFrame to a specific team.
        
        Args:
            df: Input DataFrame
            team: Team name to filter to
            team_column: Name of the column containing team values
            
        Returns:
            Filtered DataFrame
        """
        if team_column in df.columns:
            return df[df[team_column].str.lower() == team.lower()]
        return df
    
    @staticmethod
    def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names to snake_case format.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with standardized column names
        """
        # Convert camelCase to snake_case
        def camel_to_snake(name):
            import re
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        
        # Create a map of old names to new names
        col_map = {col: camel_to_snake(col) for col in df.columns}
        
        # Rename columns
        return df.rename(columns=col_map) 