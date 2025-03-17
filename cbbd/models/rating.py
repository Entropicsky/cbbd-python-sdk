"""
Models for basketball ratings data from the CFBD API.

This module contains classes for team ratings from various systems.
"""

from typing import Dict, List, Optional, Any


class SRSRating:
    """
    Represents a team's Simple Rating System (SRS) rating.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def year(self) -> Optional[int]:
        """The season year."""
        return self._data.get('year')
    
    @property
    def team(self) -> Optional[str]:
        """The team name."""
        return self._data.get('team')
    
    @property
    def conference(self) -> Optional[str]:
        """The team's conference."""
        return self._data.get('conference')
    
    @property
    def rating(self) -> Optional[float]:
        """The team's SRS rating."""
        return self._data.get('rating')
    
    @property
    def ranking(self) -> Optional[int]:
        """The team's ranking based on SRS."""
        return self._data.get('ranking')


class SRSRatingList(List[SRSRating]):
    """
    A list of SRSRating objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([SRSRating(item) for item in data])


class SPRating:
    """
    Represents a team's SP+ rating.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def year(self) -> Optional[int]:
        """The season year."""
        return self._data.get('year')
    
    @property
    def team(self) -> Optional[str]:
        """The team name."""
        return self._data.get('team')
    
    @property
    def conference(self) -> Optional[str]:
        """The team's conference."""
        return self._data.get('conference')
    
    @property
    def rating(self) -> Optional[float]:
        """The team's SP+ rating."""
        return self._data.get('rating')
    
    @property
    def ranking(self) -> Optional[int]:
        """The team's ranking based on SP+."""
        return self._data.get('ranking')
    
    @property
    def offense_rating(self) -> Optional[float]:
        """The team's offensive rating."""
        return self._data.get('offense_rating')
    
    @property
    def offense_ranking(self) -> Optional[int]:
        """The team's offensive ranking."""
        return self._data.get('offense_ranking')
    
    @property
    def defense_rating(self) -> Optional[float]:
        """The team's defensive rating."""
        return self._data.get('defense_rating')
    
    @property
    def defense_ranking(self) -> Optional[int]:
        """The team's defensive ranking."""
        return self._data.get('defense_ranking')


class SPRatingList(List[SPRating]):
    """
    A list of SPRating objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([SPRating(item) for item in data])


class EloRating:
    """
    Represents a team's Elo rating.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def year(self) -> Optional[int]:
        """The season year."""
        return self._data.get('year')
    
    @property
    def team(self) -> Optional[str]:
        """The team name."""
        return self._data.get('team')
    
    @property
    def conference(self) -> Optional[str]:
        """The team's conference."""
        return self._data.get('conference')
    
    @property
    def elo(self) -> Optional[float]:
        """The team's Elo rating."""
        return self._data.get('elo')


class EloRatingList(List[EloRating]):
    """
    A list of EloRating objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([EloRating(item) for item in data]) 