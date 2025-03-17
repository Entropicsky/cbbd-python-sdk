"""
Models for basketball statistics data from the CFBD API.

This module contains classes for team and player statistics.
"""

from typing import Dict, List, Optional, Any


class TeamStats:
    """
    Represents team statistics for a basketball game.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert team stats to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the team stats.
        """
        return self._data.copy()

    @property
    def game_id(self) -> Optional[int]:
        """The game ID."""
        return self._data.get('game_id')
    
    @property
    def team_id(self) -> Optional[int]:
        """The team ID."""
        return self._data.get('team_id')
    
    @property
    def team(self) -> Optional[str]:
        """The team name."""
        return self._data.get('team')
    
    @property
    def conference(self) -> Optional[str]:
        """The team's conference."""
        return self._data.get('conference')
    
    @property
    def home_away(self) -> Optional[str]:
        """Whether the team was home or away."""
        return self._data.get('home_away')
    
    @property
    def points(self) -> Optional[int]:
        """Total points scored."""
        return self._data.get('points')
    
    @property
    def field_goals_made(self) -> Optional[int]:
        """Field goals made."""
        return self._data.get('field_goals_made')
    
    @property
    def field_goals_attempted(self) -> Optional[int]:
        """Field goals attempted."""
        return self._data.get('field_goals_attempted')
    
    @property
    def field_goal_percentage(self) -> Optional[float]:
        """Field goal percentage."""
        return self._data.get('field_goal_percentage')
    
    @property
    def three_points_made(self) -> Optional[int]:
        """Three-point field goals made."""
        return self._data.get('three_points_made')
    
    @property
    def three_points_attempted(self) -> Optional[int]:
        """Three-point field goals attempted."""
        return self._data.get('three_points_attempted')
    
    @property
    def three_point_percentage(self) -> Optional[float]:
        """Three-point field goal percentage."""
        return self._data.get('three_point_percentage')
    
    @property
    def free_throws_made(self) -> Optional[int]:
        """Free throws made."""
        return self._data.get('free_throws_made')
    
    @property
    def free_throws_attempted(self) -> Optional[int]:
        """Free throws attempted."""
        return self._data.get('free_throws_attempted')
    
    @property
    def free_throw_percentage(self) -> Optional[float]:
        """Free throw percentage."""
        return self._data.get('free_throw_percentage')
    
    @property
    def rebounds(self) -> Optional[int]:
        """Total rebounds."""
        return self._data.get('rebounds')
    
    @property
    def offensive_rebounds(self) -> Optional[int]:
        """Offensive rebounds."""
        return self._data.get('offensive_rebounds')
    
    @property
    def defensive_rebounds(self) -> Optional[int]:
        """Defensive rebounds."""
        return self._data.get('defensive_rebounds')
    
    @property
    def assists(self) -> Optional[int]:
        """Assists."""
        return self._data.get('assists')
    
    @property
    def steals(self) -> Optional[int]:
        """Steals."""
        return self._data.get('steals')
    
    @property
    def blocks(self) -> Optional[int]:
        """Blocks."""
        return self._data.get('blocks')
    
    @property
    def turnovers(self) -> Optional[int]:
        """Turnovers."""
        return self._data.get('turnovers')
    
    @property
    def fouls(self) -> Optional[int]:
        """Personal fouls."""
        return self._data.get('fouls')
    
    @property
    def win(self) -> Optional[bool]:
        """Whether the team won the game."""
        return self._data.get('win')


class TeamStatsList(List[TeamStats]):
    """
    A list of TeamStats objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([TeamStats(item) for item in data])


class PlayerStats:
    """
    Represents player statistics for a basketball game.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert player stats to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the player stats.
        """
        return self._data.copy()

    @property
    def game_id(self) -> Optional[int]:
        """The game ID."""
        return self._data.get('game_id')
    
    @property
    def team_id(self) -> Optional[int]:
        """The team ID."""
        return self._data.get('team_id')
    
    @property
    def team(self) -> Optional[str]:
        """The team name."""
        return self._data.get('team')
    
    @property
    def conference(self) -> Optional[str]:
        """The team's conference."""
        return self._data.get('conference')
    
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
    def home_away(self) -> Optional[str]:
        """Whether the team was home or away."""
        return self._data.get('home_away')
    
    @property
    def starter(self) -> Optional[bool]:
        """Whether the player was a starter."""
        return self._data.get('starter')
    
    @property
    def minutes(self) -> Optional[int]:
        """Minutes played."""
        return self._data.get('minutes')
    
    @property
    def points(self) -> Optional[int]:
        """Points scored."""
        return self._data.get('points')
    
    @property
    def field_goals_made(self) -> Optional[int]:
        """Field goals made."""
        return self._data.get('field_goals_made')
    
    @property
    def field_goals_attempted(self) -> Optional[int]:
        """Field goals attempted."""
        return self._data.get('field_goals_attempted')
    
    @property
    def field_goal_percentage(self) -> Optional[float]:
        """Field goal percentage."""
        return self._data.get('field_goal_percentage')
    
    @property
    def three_points_made(self) -> Optional[int]:
        """Three-point field goals made."""
        return self._data.get('three_points_made')
    
    @property
    def three_points_attempted(self) -> Optional[int]:
        """Three-point field goals attempted."""
        return self._data.get('three_points_attempted')
    
    @property
    def three_point_percentage(self) -> Optional[float]:
        """Three-point field goal percentage."""
        return self._data.get('three_point_percentage')
    
    @property
    def free_throws_made(self) -> Optional[int]:
        """Free throws made."""
        return self._data.get('free_throws_made')
    
    @property
    def free_throws_attempted(self) -> Optional[int]:
        """Free throws attempted."""
        return self._data.get('free_throws_attempted')
    
    @property
    def free_throw_percentage(self) -> Optional[float]:
        """Free throw percentage."""
        return self._data.get('free_throw_percentage')
    
    @property
    def rebounds(self) -> Optional[int]:
        """Total rebounds."""
        return self._data.get('rebounds')
    
    @property
    def offensive_rebounds(self) -> Optional[int]:
        """Offensive rebounds."""
        return self._data.get('offensive_rebounds')
    
    @property
    def defensive_rebounds(self) -> Optional[int]:
        """Defensive rebounds."""
        return self._data.get('defensive_rebounds')
    
    @property
    def assists(self) -> Optional[int]:
        """Assists."""
        return self._data.get('assists')
    
    @property
    def steals(self) -> Optional[int]:
        """Steals."""
        return self._data.get('steals')
    
    @property
    def blocks(self) -> Optional[int]:
        """Blocks."""
        return self._data.get('blocks')
    
    @property
    def turnovers(self) -> Optional[int]:
        """Turnovers."""
        return self._data.get('turnovers')
    
    @property
    def fouls(self) -> Optional[int]:
        """Personal fouls."""
        return self._data.get('fouls')
    
    @property
    def plus_minus(self) -> Optional[int]:
        """Plus/minus rating."""
        return self._data.get('plus_minus')


class PlayerStatsList(List[PlayerStats]):
    """
    A list of PlayerStats objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([PlayerStats(item) for item in data])


class AdvancedTeamStats:
    """
    Represents advanced team statistics.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert advanced team stats to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the advanced team stats.
        """
        return self._data.copy()
    
    @property
    def team_id(self) -> Optional[int]:
        """The team ID."""
        return self._data.get('team_id')
    
    @property
    def team(self) -> Optional[str]:
        """The team name."""
        return self._data.get('team')
    
    @property
    def conference(self) -> Optional[str]:
        """The team's conference."""
        return self._data.get('conference')
    
    @property
    def season(self) -> Optional[int]:
        """The season year."""
        return self._data.get('season')
    
    @property
    def games(self) -> Optional[int]:
        """Number of games played."""
        return self._data.get('games')
    
    @property
    def wins(self) -> Optional[int]:
        """Number of wins."""
        return self._data.get('wins')
    
    @property
    def losses(self) -> Optional[int]:
        """Number of losses."""
        return self._data.get('losses')
    
    @property
    def offensive_efficiency(self) -> Optional[float]:
        """Offensive efficiency rating."""
        return self._data.get('offensive_efficiency')
    
    @property
    def defensive_efficiency(self) -> Optional[float]:
        """Defensive efficiency rating."""
        return self._data.get('defensive_efficiency')
    
    @property
    def tempo(self) -> Optional[float]:
        """Tempo (possessions per 40 minutes)."""
        return self._data.get('tempo')
    
    @property
    def effective_field_goal_percentage(self) -> Optional[float]:
        """Effective field goal percentage."""
        return self._data.get('effective_field_goal_percentage')
    
    @property
    def turnover_percentage(self) -> Optional[float]:
        """Turnover percentage."""
        return self._data.get('turnover_percentage')
    
    @property
    def offensive_rebound_percentage(self) -> Optional[float]:
        """Offensive rebound percentage."""
        return self._data.get('offensive_rebound_percentage')
    
    @property
    def free_throw_rate(self) -> Optional[float]:
        """Free throw rate."""
        return self._data.get('free_throw_rate')
    
    @property
    def three_point_percentage(self) -> Optional[float]:
        """Three-point field goal percentage."""
        return self._data.get('three_point_percentage')
    
    @property
    def two_point_percentage(self) -> Optional[float]:
        """Two-point field goal percentage."""
        return self._data.get('two_point_percentage')


class AdvancedTeamStatsList(List[AdvancedTeamStats]):
    """
    A list of AdvancedTeamStats objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([AdvancedTeamStats(item) for item in data]) 