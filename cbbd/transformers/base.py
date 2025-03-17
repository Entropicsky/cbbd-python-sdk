"""
Base transformer module providing the foundation for data transformations.

This module contains the BaseTransformer class which establishes the
common interface and utilities used by all transformer classes.
"""

import pandas as pd
import numpy as np
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

class BaseTransformer:
    """
    Base class for all data transformers.
    
    This class provides common functionality and defines the interface
    that all transformer classes should implement.
    """
    
    @staticmethod
    def clean_null_values(value: Any) -> Any:
        """
        Convert string "NULL" values to proper Python None values.
        
        Args:
            value: The value to clean
            
        Returns:
            The cleaned value (None if it was "NULL", unchanged otherwise)
        """
        if isinstance(value, str) and value.upper() == "NULL":
            return None
        return value
    
    @staticmethod
    def extract_nested_value(data: Dict, key_path: str, default: Any = None) -> Any:
        """
        Extract a value from a nested dictionary structure using a dot-notation path.
        
        Args:
            data: Dictionary to extract from
            key_path: Dot-notation path (e.g., "hometown.city")
            default: Default value if the path doesn't exist
            
        Returns:
            The extracted value or the default
        """
        if not data:
            return default
            
        keys = key_path.split('.')
        result = data
        
        try:
            for key in keys:
                if isinstance(result, dict):
                    result = result.get(key, {})
                else:
                    return default
                    
            # Check if we ended up with an empty dict or the string "NULL"
            if result == {} or (isinstance(result, str) and result.upper() == "NULL"):
                return default
                
            return result
        except Exception:
            return default
    
    @staticmethod
    def flatten_dict(data: Dict, 
                     parent_key: str = '', 
                     sep: str = '_') -> Dict:
        """
        Flatten a nested dictionary structure.
        
        Args:
            data: Dictionary to flatten
            parent_key: Prefix for flattened keys
            sep: Separator to use between nested keys
            
        Returns:
            A flattened dictionary
        """
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(BaseTransformer.flatten_dict(v, new_key, sep).items())
            else:
                items.append((new_key, v))
                
        return dict(items)
    
    @staticmethod
    def safe_convert_to_numeric(df: pd.DataFrame, 
                               columns: List[str]) -> pd.DataFrame:
        """
        Safely convert dataframe columns to numeric types.
        
        Args:
            df: DataFrame to modify
            columns: List of column names to convert
            
        Returns:
            Modified DataFrame with numeric columns
        """
        result = df.copy()
        
        for col in columns:
            if col in result.columns:
                # Handle 'NULL' strings before conversion
                result[col] = result[col].replace('NULL', np.nan)
                # Convert to numeric
                result[col] = pd.to_numeric(result[col], errors='coerce')
                
        return result
    
    @staticmethod
    def apply_defaults(df: pd.DataFrame, 
                       defaults: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply default values to missing values in DataFrame.
        
        Args:
            df: DataFrame to modify
            defaults: Dictionary mapping column names to default values
            
        Returns:
            Modified DataFrame with defaults applied
        """
        result = df.copy()
        
        for col, default in defaults.items():
            if col in result.columns:
                result[col] = result[col].fillna(default)
                
        return result
    
    @staticmethod
    def to_dataframe(data: Any) -> pd.DataFrame:
        """
        Convert data to a pandas DataFrame.
        
        This is an abstract method that should be implemented by subclasses.
        
        Args:
            data: The data to convert
            
        Returns:
            A pandas DataFrame
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement to_dataframe()") 