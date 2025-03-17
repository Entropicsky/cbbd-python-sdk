"""
Models for basketball betting lines data from the CFBD API.

This module contains classes for betting lines and odds.
"""

from typing import Dict, List, Optional, Any


class Line:
    """
    Represents betting lines for a basketball game.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def game_id(self) -> Optional[int]:
        """The game ID."""
        return self._data.get('game_id')
    
    @property
    def home_team(self) -> Optional[str]:
        """The home team name."""
        return self._data.get('home_team')
    
    @property
    def away_team(self) -> Optional[str]:
        """The away team name."""
        return self._data.get('away_team')
    
    @property
    def provider(self) -> Optional[str]:
        """The betting line provider."""
        return self._data.get('provider')
    
    @property
    def spread(self) -> Optional[float]:
        """The point spread."""
        return self._data.get('spread')
    
    @property
    def over_under(self) -> Optional[float]:
        """The over/under total."""
        return self._data.get('over_under')
    
    @property
    def home_moneyline(self) -> Optional[int]:
        """The home team moneyline."""
        return self._data.get('home_moneyline')
    
    @property
    def away_moneyline(self) -> Optional[int]:
        """The away team moneyline."""
        return self._data.get('away_moneyline')
    
    @property
    def formatted_spread(self) -> Optional[str]:
        """The formatted point spread."""
        return self._data.get('formatted_spread')
    
    @property
    def formatted_over_under(self) -> Optional[str]:
        """The formatted over/under total."""
        return self._data.get('formatted_over_under')


class LineList(List[Line]):
    """
    A list of Line objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([Line(item) for item in data]) 