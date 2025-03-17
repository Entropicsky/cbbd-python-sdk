"""
Base model classes for the CBBD Python SDK.

This module contains base model classes used throughout the SDK.
"""

from typing import Dict, Any, Optional


class BaseModel:
    """
    Base class for all CBBD models to provide common functionality.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data or {}
    
    def __str__(self) -> str:
        """String representation of the model."""
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.get_base_properties().items()])})"
    
    def get_raw_data(self) -> Dict[str, Any]:
        """
        Get the raw data dictionary for debugging and inspection.
        
        Returns:
            Dict[str, Any]: The raw data dictionary.
        """
        return self._data
    
    def get_base_properties(self) -> Dict[str, Any]:
        """
        Get basic properties for string representation.
        Override in subclasses for better string representations.
        
        Returns:
            Dict[str, Any]: Dictionary of important properties.
        """
        return {'id': self._data.get('id')}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the model.
        """
        return self._data.copy()

class BaseModelList:
    """
    List of base models.
    
    Attributes:
        _data (list): List of raw data from API
        _model_class (class): Model class to use for items
    """
    
    def __init__(self, data, model_class):
        """
        Initialize the model list.
        
        Args:
            data (list): List of raw data from API
            model_class (class): Model class to use for items
        """
        self._data = data
        self._model_class = model_class
        self._models = [model_class(item) for item in data]
    
    def __getitem__(self, index):
        """Get item at index."""
        return self._models[index]
    
    def __len__(self):
        """Get length of list."""
        return len(self._models)
    
    def __iter__(self):
        """Iterate over models."""
        return iter(self._models)
    
    def to_dict(self):
        """
        Convert to list of dictionaries.
        
        Returns:
            list: List of dictionary representations
        """
        return [model.to_dict() for model in self._models]
    
    def to_dataframe(self):
        """
        Convert to pandas DataFrame if pandas is available.
        
        Returns:
            pandas.DataFrame: DataFrame representation
        
        Raises:
            ImportError: If pandas is not installed
        """
        try:
            import pandas as pd
            return pd.DataFrame(self._data)
        except ImportError:
            raise ImportError("pandas is required for DataFrame conversion. Install it with 'pip install pandas'.") 