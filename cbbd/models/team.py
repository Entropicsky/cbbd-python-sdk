"""
Team models for the CFBD Python SDK.
"""

from .base import BaseModel, BaseModelList

class Team(BaseModel):
    """
    Team model.
    
    Represents a college basketball team.
    """
    
    @property
    def id(self):
        """Get team ID."""
        return self._data.get('id')
    
    @property
    def source_id(self):
        """Get source ID."""
        return self._data.get('sourceId')
    
    @property
    def name(self):
        """Get team name."""
        return self._data.get('school')
    
    @property
    def mascot(self):
        """Get team mascot."""
        return self._data.get('mascot')
    
    @property
    def abbreviation(self):
        """Get team abbreviation."""
        return self._data.get('abbreviation')
    
    @property
    def display_name(self):
        """Get team display name."""
        return self._data.get('displayName')
    
    @property
    def short_display_name(self):
        """Get team short display name."""
        return self._data.get('shortDisplayName')
    
    @property
    def primary_color(self):
        """Get team primary color."""
        return self._data.get('primaryColor')
    
    @property
    def secondary_color(self):
        """Get team secondary color."""
        return self._data.get('secondaryColor')
    
    @property
    def venue_id(self):
        """Get venue ID."""
        return self._data.get('currentVenueId')
    
    @property
    def venue(self):
        """Get venue name."""
        return self._data.get('currentVenue')
    
    @property
    def city(self):
        """Get team city."""
        return self._data.get('currentCity')
    
    @property
    def state(self):
        """Get team state."""
        return self._data.get('currentState')
    
    @property
    def conference_id(self):
        """Get conference ID."""
        return self._data.get('conferenceId')
    
    @property
    def conference(self):
        """Get conference name."""
        return self._data.get('conference')

class TeamList(BaseModelList):
    """List of Team objects."""
    
    def __init__(self, data):
        """
        Initialize the team list.
        
        Args:
            data (list): List of team data from API
        """
        super().__init__(data, Team)

class TeamRoster(BaseModel):
    """
    Team roster model.
    
    Represents a team's roster for a specific season.
    """
    
    @property
    def team_id(self):
        """Get team ID."""
        return self._data.get('teamId')
    
    @property
    def team(self):
        """Get team name."""
        return self._data.get('team')
    
    @property
    def season(self):
        """Get season."""
        return self._data.get('season')
    
    @property
    def players(self):
        """Get list of players."""
        return [Player(player) for player in self._data.get('players', [])]

class Player(BaseModel):
    """
    Player model.
    
    Represents a player on a team roster.
    """
    
    @property
    def id(self):
        """Get player ID."""
        return self._data.get('id')
    
    @property
    def name(self):
        """Get player name."""
        return self._data.get('name')
    
    @property
    def position(self):
        """Get player position."""
        return self._data.get('position')
    
    @property
    def jersey(self):
        """Get player jersey number."""
        return self._data.get('jersey')
    
    @property
    def height(self):
        """Get player height."""
        return self._data.get('height')
    
    @property
    def weight(self):
        """Get player weight."""
        return self._data.get('weight')
    
    @property
    def year(self):
        """Get player year/class."""
        return self._data.get('year')
    
    @property
    def hometown(self):
        """Get player hometown."""
        return self._data.get('hometown')
    
    @property
    def home_state(self):
        """Get player home state."""
        return self._data.get('homeState')
    
    @property
    def home_country(self):
        """Get player home country."""
        return self._data.get('homeCountry') 