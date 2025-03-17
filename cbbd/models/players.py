"""
Models for player data.
"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import date

from .base import BaseModel


@dataclass
class Hometown:
    """
    Model representing a player's hometown information.
    """
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    county_fips: Optional[str] = None


@dataclass
class Player(BaseModel):
    """
    Model representing a player.
    """
    id: int = None
    source_id: str = None
    name: str = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    jersey: Optional[str] = None
    position: Optional[str] = None
    height: Optional[int] = None  # in inches
    weight: Optional[int] = None  # in pounds
    hometown: Optional[Hometown] = None
    date_of_birth: Optional[date] = None
    start_season: Optional[int] = None
    end_season: Optional[int] = None
    team_id: Optional[int] = None
    team: Optional[str] = None
    conference: Optional[str] = None
    _raw_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """
        Process raw data after initialization.
        """
        super().__post_init__()

        # Process hometown data if available
        if self._raw_data and 'hometown' in self._raw_data and self._raw_data['hometown']:
            hometown_data = self._raw_data['hometown']
            self.hometown = Hometown(
                city=hometown_data.get('city'),
                state=hometown_data.get('state'),
                country=hometown_data.get('country'),
                latitude=hometown_data.get('latitude'),
                longitude=hometown_data.get('longitude'),
                county_fips=hometown_data.get('countyFips')
            )
            
        # Convert date of birth string to date object if available
        if isinstance(self.date_of_birth, str):
            try:
                self.date_of_birth = date.fromisoformat(self.date_of_birth)
            except (ValueError, TypeError):
                self.date_of_birth = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """
        Create a Player instance from a dictionary.
        
        Args:
            data: Dictionary containing player data.
            
        Returns:
            A Player instance.
        """
        player = cls()
        player._raw_data = data.copy()
        
        # Extract fields using camelCase to snake_case conversion
        player.id = data.get('id')
        player.source_id = data.get('sourceId')
        player.name = data.get('name')
        player.first_name = data.get('firstName')
        player.last_name = data.get('lastName')
        player.jersey = data.get('jersey')
        player.position = data.get('position')
        player.height = data.get('height')
        player.weight = data.get('weight')
        player.date_of_birth = data.get('dateOfBirth')
        player.start_season = data.get('startSeason')
        player.end_season = data.get('endSeason')
        
        # Process hometown data
        player.__post_init__()
        
        return player
        
    def get_raw_data(self) -> Dict[str, Any]:
        """
        Get the raw data dictionary for this player.
        
        Returns:
            The raw data dictionary.
        """
        return self._raw_data 