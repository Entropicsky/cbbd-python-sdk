"""
Models for basketball lineup data from the CFBD API.

This module contains classes for team lineups and player combinations.
"""

from typing import Dict, List, Optional, Any


class Lineup:
    """
    Represents a team lineup or player combination.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def game_id(self) -> Optional[int]:
        """The game ID."""
        return self._data.get('game_id')
    
    @property
    def team(self) -> Optional[str]:
        """The team name."""
        return self._data.get('team')
    
    @property
    def players(self) -> List[str]:
        """The list of players in the lineup."""
        return self._data.get('players', [])
    
    @property
    def minutes(self) -> Optional[float]:
        """Minutes played by this lineup."""
        return self._data.get('minutes')
    
    @property
    def possessions(self) -> Optional[int]:
        """Number of possessions with this lineup."""
        return self._data.get('possessions')
    
    @property
    def points(self) -> Optional[int]:
        """Points scored by this lineup."""
        return self._data.get('points')
    
    @property
    def points_allowed(self) -> Optional[int]:
        """Points allowed by this lineup."""
        return self._data.get('points_allowed')
    
    @property
    def efficiency(self) -> Optional[float]:
        """Offensive efficiency of this lineup."""
        return self._data.get('efficiency')
    
    @property
    def defensive_efficiency(self) -> Optional[float]:
        """Defensive efficiency of this lineup."""
        return self._data.get('defensive_efficiency')
    
    @property
    def net_efficiency(self) -> Optional[float]:
        """Net efficiency of this lineup."""
        return self._data.get('net_efficiency')


class LineupList(List[Lineup]):
    """
    A list of Lineup objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([Lineup(item) for item in data]) 