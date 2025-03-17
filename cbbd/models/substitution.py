"""
Models for basketball substitution data from the CFBD API.

This module contains classes for player substitutions.
"""

from typing import Dict, List, Optional, Any


class Substitution:
    """
    Represents a player substitution in a basketball game.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def game_id(self) -> Optional[int]:
        """The game ID."""
        return self._data.get('game_id')
    
    @property
    def period(self) -> Optional[int]:
        """The period number."""
        return self._data.get('period')
    
    @property
    def clock(self) -> Optional[str]:
        """The game clock at the time of the substitution."""
        return self._data.get('clock')
    
    @property
    def team_id(self) -> Optional[int]:
        """The ID of the team making the substitution."""
        return self._data.get('team_id')
    
    @property
    def team(self) -> Optional[str]:
        """The name of the team making the substitution."""
        return self._data.get('team')
    
    @property
    def player_in_id(self) -> Optional[int]:
        """The ID of the player entering the game."""
        return self._data.get('player_in_id')
    
    @property
    def player_in(self) -> Optional[str]:
        """The name of the player entering the game."""
        return self._data.get('player_in')
    
    @property
    def player_out_id(self) -> Optional[int]:
        """The ID of the player leaving the game."""
        return self._data.get('player_out_id')
    
    @property
    def player_out(self) -> Optional[str]:
        """The name of the player leaving the game."""
        return self._data.get('player_out')
    
    @property
    def home_score(self) -> Optional[int]:
        """The home team's score at the time of the substitution."""
        return self._data.get('home_score')
    
    @property
    def away_score(self) -> Optional[int]:
        """The away team's score at the time of the substitution."""
        return self._data.get('away_score')


class SubstitutionList(List[Substitution]):
    """
    A list of Substitution objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([Substitution(item) for item in data]) 