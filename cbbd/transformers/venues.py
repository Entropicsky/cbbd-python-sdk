"""
Transformers for venue data.
"""
import logging
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from ..models.venue import Venue
from .base import BaseTransformer

logger = logging.getLogger(__name__)

class VenuesTransformer(BaseTransformer):
    """
    Transformer for venue data.
    """
    
    def to_dataframe(self, data: Any) -> pd.DataFrame:
        """
        Convert venue data to a pandas DataFrame.
        
        Args:
            data: Venue data to convert, can be a list of Venue objects or raw dictionaries.
            
        Returns:
            A pandas DataFrame containing the venue data.
        """
        if not data:
            logger.warning("No data provided to transform")
            return pd.DataFrame()
            
        try:
            venues_data = []
            
            # Process raw API responses or Venue objects
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, Venue):
                        venues_data.append(self._venue_to_dict(item))
                    elif isinstance(item, dict):
                        venues_data.append(item)
                    else:
                        logger.warning(f"Unexpected item type in venue data: {type(item)}")
            elif isinstance(data, Venue):
                venues_data.append(self._venue_to_dict(data))
            else:
                logger.warning(f"Unsupported data type for venue transformation: {type(data)}")
                return pd.DataFrame()
                
            if not venues_data:
                logger.warning("No valid venue data found to transform")
                return pd.DataFrame()
                
            # Convert to DataFrame
            df = pd.DataFrame(venues_data)
            
            # Clean NULL values
            for col in df.columns:
                df[col] = df[col].apply(self.clean_null_values)
                
            # Convert numeric columns
            if 'capacity' in df.columns:
                df['capacity'] = pd.to_numeric(df['capacity'], errors='coerce')
                
            # Standardize column names (convert camelCase to snake_case)
            df.columns = [col[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in col[1:]]) for col in df.columns]
                
            return df
            
        except Exception as e:
            logger.error(f"Error transforming venue data to DataFrame: {e}")
            return pd.DataFrame()
            
    def _venue_to_dict(self, venue: Venue) -> Dict:
        """
        Convert a Venue object to a dictionary.
        
        Args:
            venue: The Venue object to convert.
            
        Returns:
            A dictionary representation of the venue.
        """
        if not venue:
            return {}
            
        venue_dict = {
            'id': venue.id,
            'source_id': venue.source_id,
            'name': venue.name,
            'city': venue.city,
            'state': venue.state,
            'country': venue.country,
            'capacity': venue.capacity,
            'indoor': venue.indoor
        }
            
        return venue_dict 