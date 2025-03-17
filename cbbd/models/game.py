"""
Game models for the CFBD Python SDK.
"""

from datetime import datetime
from .base import BaseModel, BaseModelList

class Game(BaseModel):
    """
    Game model.
    
    Represents a college basketball game.
    """
    
    @property
    def id(self):
        """Get game ID."""
        return self._data.get('id')
    
    @property
    def source_id(self):
        """Get source ID."""
        return self._data.get('sourceId')
    
    @property
    def season(self):
        """Get season."""
        return self._data.get('season')
    
    @property
    def season_label(self):
        """Get season label."""
        return self._data.get('seasonLabel')
    
    @property
    def season_type(self):
        """Get season type."""
        return self._data.get('seasonType')
    
    @property
    def tournament(self):
        """Get tournament name."""
        return self._data.get('tournament')
    
    @property
    def start_date(self):
        """
        Get start date.
        
        Returns:
            datetime: Start date as datetime object
        """
        date_str = self._data.get('startDate')
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return None
        return None
    
    @property
    def start_time_tbd(self):
        """Get whether start time is TBD."""
        return self._data.get('startTimeTbd')
    
    @property
    def neutral_site(self):
        """Get whether game is at a neutral site."""
        return self._data.get('neutralSite')
    
    @property
    def conference_game(self):
        """Get whether game is a conference game."""
        return self._data.get('conferenceGame')
    
    @property
    def game_type(self):
        """Get game type."""
        return self._data.get('gameType')
    
    @property
    def status(self):
        """Get game status."""
        return self._data.get('status')
    
    @property
    def game_notes(self):
        """Get game notes."""
        return self._data.get('gameNotes')
    
    @property
    def attendance(self):
        """Get attendance."""
        return self._data.get('attendance')
    
    @property
    def home_team_id(self):
        """Get home team ID."""
        return self._data.get('homeTeamId')
    
    @property
    def home_team(self):
        """Get home team name."""
        return self._data.get('homeTeam')
    
    @property
    def home_conference_id(self):
        """Get home conference ID."""
        return self._data.get('homeConferenceId')
    
    @property
    def home_conference(self):
        """Get home conference name."""
        return self._data.get('homeConference')
    
    @property
    def home_seed(self):
        """Get home team seed."""
        return self._data.get('homeSeed')
    
    @property
    def home_points(self):
        """Get home team points."""
        return self._data.get('homePoints')
    
    @property
    def home_period_points(self):
        """Get home team period points."""
        return self._data.get('homePeriodPoints')
    
    @property
    def home_winner(self):
        """Get whether home team won."""
        return self._data.get('homeWinner')
    
    @property
    def away_team_id(self):
        """Get away team ID."""
        return self._data.get('awayTeamId')
    
    @property
    def away_team(self):
        """Get away team name."""
        return self._data.get('awayTeam')
    
    @property
    def away_conference_id(self):
        """Get away conference ID."""
        return self._data.get('awayConferenceId')
    
    @property
    def away_conference(self):
        """Get away conference name."""
        return self._data.get('awayConference')
    
    @property
    def away_seed(self):
        """Get away team seed."""
        return self._data.get('awaySeed')
    
    @property
    def away_points(self):
        """Get away team points."""
        return self._data.get('awayPoints')
    
    @property
    def away_period_points(self):
        """Get away team period points."""
        return self._data.get('awayPeriodPoints')
    
    @property
    def away_winner(self):
        """Get whether away team won."""
        return self._data.get('awayWinner')
    
    @property
    def excitement(self):
        """Get excitement index."""
        return self._data.get('excitement')
    
    @property
    def venue_id(self):
        """Get venue ID."""
        return self._data.get('venueId')
    
    @property
    def venue(self):
        """Get venue name."""
        return self._data.get('venue')
    
    @property
    def city(self):
        """Get city."""
        return self._data.get('city')
    
    @property
    def state(self):
        """Get state."""
        return self._data.get('state')
    
    @property
    def winner(self):
        """
        Get winner team name.
        
        Returns:
            str: Name of winning team
        """
        if self.home_winner:
            return self.home_team
        elif self.away_winner:
            return self.away_team
        return None
    
    @property
    def loser(self):
        """
        Get loser team name.
        
        Returns:
            str: Name of losing team
        """
        if self.home_winner:
            return self.away_team
        elif self.away_winner:
            return self.home_team
        return None
    
    @property
    def score_display(self):
        """
        Get score display.
        
        Returns:
            str: Score display (e.g., "Duke 80, UNC 70")
        """
        if self.home_points is not None and self.away_points is not None:
            return f"{self.home_team} {self.home_points}, {self.away_team} {self.away_points}"
        return None

class GameList(BaseModelList):
    """List of Game objects."""
    
    def __init__(self, data):
        """
        Initialize the game list.
        
        Args:
            data (list): List of game data from API
        """
        super().__init__(data, Game)

class GameMedia(BaseModel):
    """
    Game media model.
    
    Represents media/broadcast information for a game.
    """
    
    @property
    def game_id(self):
        """Get game ID."""
        return self._data.get('gameId')
    
    @property
    def source_id(self):
        """Get source ID."""
        return self._data.get('sourceId')
    
    @property
    def home_team(self):
        """Get home team name."""
        return self._data.get('homeTeam')
    
    @property
    def away_team(self):
        """Get away team name."""
        return self._data.get('awayTeam')
    
    @property
    def outlet(self):
        """Get media outlet."""
        return self._data.get('outlet')

class GameMediaList(BaseModelList):
    """List of GameMedia objects."""
    
    def __init__(self, data):
        """
        Initialize the game media list.
        
        Args:
            data (list): List of game media data from API
        """
        super().__init__(data, GameMedia) 