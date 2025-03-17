"""
Models for basketball play-by-play data from the CBBD API.

This module contains classes for play-by-play data.
"""

from typing import Dict, List, Optional, Any


class Play:
    """
    Represents a single play in a basketball game.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data
    
    def __str__(self):
        return f"Play(id={self.id}, type={self.play_type}, game_id={self.game_id})"
        
    def get_raw_data(self) -> Dict[str, Any]:
        """Return the raw data dictionary for debugging"""
        return self._data

    @property
    def id(self) -> Optional[int]:
        """The play ID."""
        return self._data.get('id')
    
    @property
    def game_id(self) -> Optional[int]:
        """The game ID."""
        return self._data.get('gameId') or self._data.get('game_id')
    
    @property
    def period(self) -> Optional[int]:
        """The period number."""
        return self._data.get('period')
    
    @property
    def clock(self) -> Optional[str]:
        """The game clock at the time of the play."""
        return self._data.get('clock')
    
    @property
    def shot_clock(self) -> Optional[str]:
        """The shot clock at the time of the play."""
        return self._data.get('shot_clock')
    
    @property
    def team_id(self) -> Optional[int]:
        """The ID of the team involved in the play."""
        return self._data.get('teamId') or self._data.get('team_id')
    
    @property
    def team(self) -> Optional[str]:
        """The name of the team involved in the play."""
        return self._data.get('team')
    
    @property
    def player_id(self) -> Optional[int]:
        """The ID of the player involved in the play."""
        return self._data.get('playerId') or self._data.get('player_id')
    
    @property
    def player(self) -> Optional[str]:
        """The name of the player involved in the play."""
        # Try different keys the API might use
        for key in ['player', 'athlete', 'name']:
            if key in self._data:
                return self._data.get(key)
        
        # Check participants
        participants = self._data.get('participants', [])
        if participants and len(participants) > 0 and isinstance(participants[0], dict):
            return participants[0].get('name')
        
        return None
    
    @property
    def event_type(self) -> Optional[str]:
        """The type of event (e.g., shot, rebound, foul)."""
        return self._data.get('event_type') or self._data.get('playType')
    
    @property
    def play_type(self) -> Optional[str]:
        """The type of play."""
        return self._data.get('playType')
    
    @property
    def event_subtype(self) -> Optional[str]:
        """The subtype of the event (e.g., 2-pointer, 3-pointer)."""
        return self._data.get('event_subtype')
    
    @property
    def coordinates_x(self) -> Optional[float]:
        """The x-coordinate of the play on the court."""
        return self._data.get('coordinates_x')
    
    @property
    def coordinates_y(self) -> Optional[float]:
        """The y-coordinate of the play on the court."""
        return self._data.get('coordinates_y')
    
    @property
    def home_score(self) -> Optional[int]:
        """The home team's score after the play."""
        return self._data.get('homeScore') or self._data.get('home_score')
    
    @property
    def away_score(self) -> Optional[int]:
        """The away team's score after the play."""
        return self._data.get('awayScore') or self._data.get('away_score')
    
    @property
    def description(self) -> Optional[str]:
        """A description of the play."""
        return self._data.get('description') or self._data.get('playText')
    
    @property
    def play_text(self) -> Optional[str]:
        """Text description of the play."""
        return self._data.get('playText')
    
    @property
    def sequence_number(self) -> Optional[int]:
        """The sequence number of the play in the game."""
        return self._data.get('sequence_number')
    
    @property
    def scoring_play(self) -> Optional[bool]:
        """Whether this is a scoring play."""
        return self._data.get('scoringPlay')
    
    @property
    def shooting_play(self) -> Optional[bool]:
        """Whether this is a shooting play."""
        return self._data.get('shootingPlay')


class PlayList(List[Play]):
    """
    A list of Play objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([Play(item) for item in data])


class PlayType:
    """
    Represents a type of play.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def id(self) -> Optional[int]:
        """The play type ID."""
        return self._data.get('id')
    
    @property
    def text(self) -> Optional[str]:
        """The play type text."""
        return self._data.get('text')
    
    @property
    def abbreviation(self) -> Optional[str]:
        """The play type abbreviation."""
        return self._data.get('abbreviation')


class PlayTypeList(List[PlayType]):
    """
    A list of PlayType objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([PlayType(item) for item in data]) 