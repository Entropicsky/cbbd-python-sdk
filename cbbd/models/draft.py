"""
Models for basketball draft data from the CFBD API.

This module contains classes for NBA draft picks.
"""

from typing import Dict, List, Optional, Any


class DraftPick:
    """
    Represents an NBA draft pick.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def player_id(self) -> Optional[int]:
        """The player ID."""
        return self._data.get('player_id')
    
    @property
    def player(self) -> Optional[str]:
        """The player name."""
        return self._data.get('player')
    
    @property
    def position(self) -> Optional[str]:
        """The player's position."""
        return self._data.get('position')
    
    @property
    def height(self) -> Optional[str]:
        """The player's height."""
        return self._data.get('height')
    
    @property
    def weight(self) -> Optional[int]:
        """The player's weight."""
        return self._data.get('weight')
    
    @property
    def college_team(self) -> Optional[str]:
        """The player's college team."""
        return self._data.get('college_team')
    
    @property
    def college_conference(self) -> Optional[str]:
        """The player's college conference."""
        return self._data.get('college_conference')
    
    @property
    def nba_team(self) -> Optional[str]:
        """The NBA team that drafted the player."""
        return self._data.get('nba_team')
    
    @property
    def draft_year(self) -> Optional[int]:
        """The year of the draft."""
        return self._data.get('draft_year')
    
    @property
    def draft_round(self) -> Optional[int]:
        """The round of the draft pick."""
        return self._data.get('draft_round')
    
    @property
    def draft_pick(self) -> Optional[int]:
        """The overall pick number."""
        return self._data.get('draft_pick')


class DraftPickList(List[DraftPick]):
    """
    A list of DraftPick objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([DraftPick(item) for item in data]) 