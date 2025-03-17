"""
Models for basketball recruiting data from the CFBD API.

This module contains classes for recruiting data.
"""

from typing import Dict, List, Optional, Any


class Recruit:
    """
    Represents a basketball recruit.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def id(self) -> Optional[int]:
        """The recruit ID."""
        return self._data.get('id')
    
    @property
    def name(self) -> Optional[str]:
        """The recruit's name."""
        return self._data.get('name')
    
    @property
    def position(self) -> Optional[str]:
        """The recruit's position."""
        return self._data.get('position')
    
    @property
    def height(self) -> Optional[str]:
        """The recruit's height."""
        return self._data.get('height')
    
    @property
    def weight(self) -> Optional[int]:
        """The recruit's weight."""
        return self._data.get('weight')
    
    @property
    def stars(self) -> Optional[int]:
        """The recruit's star rating."""
        return self._data.get('stars')
    
    @property
    def rating(self) -> Optional[float]:
        """The recruit's numerical rating."""
        return self._data.get('rating')
    
    @property
    def city(self) -> Optional[str]:
        """The recruit's hometown city."""
        return self._data.get('city')
    
    @property
    def state(self) -> Optional[str]:
        """The recruit's hometown state."""
        return self._data.get('state')
    
    @property
    def country(self) -> Optional[str]:
        """The recruit's home country."""
        return self._data.get('country')
    
    @property
    def school(self) -> Optional[str]:
        """The recruit's high school."""
        return self._data.get('school')
    
    @property
    def committed_to(self) -> Optional[str]:
        """The college team the recruit committed to."""
        return self._data.get('committed_to')
    
    @property
    def year(self) -> Optional[int]:
        """The recruiting class year."""
        return self._data.get('year')


class RecruitList(List[Recruit]):
    """
    A list of Recruit objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([Recruit(item) for item in data])


class TeamRecruitingRank:
    """
    Represents a team's recruiting class ranking.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def team(self) -> Optional[str]:
        """The team name."""
        return self._data.get('team')
    
    @property
    def conference(self) -> Optional[str]:
        """The team's conference."""
        return self._data.get('conference')
    
    @property
    def year(self) -> Optional[int]:
        """The recruiting class year."""
        return self._data.get('year')
    
    @property
    def rank(self) -> Optional[int]:
        """The team's recruiting class rank."""
        return self._data.get('rank')
    
    @property
    def total_points(self) -> Optional[float]:
        """The team's total recruiting points."""
        return self._data.get('total_points')
    
    @property
    def average_rating(self) -> Optional[float]:
        """The team's average recruit rating."""
        return self._data.get('average_rating')
    
    @property
    def commits(self) -> Optional[int]:
        """The number of commits in the team's recruiting class."""
        return self._data.get('commits')


class TeamRecruitingRankList(List[TeamRecruitingRank]):
    """
    A list of TeamRecruitingRank objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([TeamRecruitingRank(item) for item in data]) 