"""
Models for basketball rankings data from the CFBD API.

This module contains classes for team rankings from various polls.
"""

from typing import Dict, List, Optional, Any


class RankingTeam:
    """
    Represents a team's ranking in a poll.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def rank(self) -> Optional[int]:
        """The team's rank in the poll."""
        return self._data.get('rank')
    
    @property
    def school(self) -> Optional[str]:
        """The school/team name."""
        return self._data.get('school')
    
    @property
    def conference(self) -> Optional[str]:
        """The team's conference."""
        return self._data.get('conference')
    
    @property
    def first_place_votes(self) -> Optional[int]:
        """Number of first place votes received."""
        return self._data.get('firstPlaceVotes')
    
    @property
    def points(self) -> Optional[int]:
        """Total points received in the poll."""
        return self._data.get('points')


class RankingTeamList(List[RankingTeam]):
    """
    A list of RankingTeam objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([RankingTeam(item) for item in data])


class RankingPoll:
    """
    Represents a ranking poll (e.g., AP Top 25, Coaches Poll).
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def poll(self) -> Optional[str]:
        """The name of the poll."""
        return self._data.get('poll')
    
    @property
    def poll_type(self) -> Optional[str]:
        """The type of poll (e.g., 'ap', 'coaches')."""
        return self._data.get('pollType')
    
    @property
    def ranks(self) -> RankingTeamList:
        """The list of ranked teams."""
        ranks_data = self._data.get('ranks', [])
        return RankingTeamList(ranks_data)


class RankingPollList(List[RankingPoll]):
    """
    A list of RankingPoll objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([RankingPoll(item) for item in data])


class Ranking:
    """
    Represents a set of rankings for a specific week and season.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def season(self) -> Optional[int]:
        """The season year."""
        return self._data.get('season')
    
    @property
    def season_type(self) -> Optional[str]:
        """The season type (regular or postseason)."""
        return self._data.get('seasonType')
    
    @property
    def week(self) -> Optional[int]:
        """The week number."""
        return self._data.get('week')
    
    @property
    def polls(self) -> RankingPollList:
        """The list of polls for this ranking."""
        polls_data = self._data.get('polls', [])
        return RankingPollList(polls_data)


class RankingList(List[Ranking]):
    """
    A list of Ranking objects.
    """
    def __init__(self, data: List[Dict[str, Any]]):
        super().__init__([Ranking(item) for item in data]) 