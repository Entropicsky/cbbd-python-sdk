"""
Models for venue data.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

from .base import BaseModel


@dataclass
class Venue(BaseModel):
    """
    Model representing a venue.
    """
    id: int = None
    source_id: str = None
    name: str = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    capacity: Optional[int] = None
    indoor: Optional[bool] = None
    _raw_data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Venue':
        """
        Create a Venue instance from a dictionary.
        
        Args:
            data: Dictionary containing venue data.
            
        Returns:
            A Venue instance.
        """
        venue = cls()
        venue._raw_data = data.copy()
        
        # Extract fields using camelCase to snake_case conversion
        venue.id = data.get('id')
        venue.source_id = data.get('sourceId')
        venue.name = data.get('name')
        venue.city = data.get('city')
        venue.state = data.get('state')
        venue.country = data.get('country')
        venue.capacity = data.get('capacity')
        venue.indoor = data.get('indoor')
        
        return venue
        
    def get_raw_data(self) -> Dict[str, Any]:
        """
        Get the raw data dictionary for this venue.
        
        Returns:
            The raw data dictionary.
        """
        return self._raw_data 