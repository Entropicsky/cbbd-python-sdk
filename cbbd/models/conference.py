"""
Conference models for the CFBD Python SDK.
"""

from .base import BaseModel, BaseModelList

class Conference(BaseModel):
    """
    Conference model.
    
    Represents a college basketball conference.
    """
    
    @property
    def id(self):
        """Get conference ID."""
        return self._data.get('id')
    
    @property
    def source_id(self):
        """Get source ID."""
        return self._data.get('sourceId')
    
    @property
    def name(self):
        """Get conference name."""
        return self._data.get('name')
    
    @property
    def abbreviation(self):
        """Get conference abbreviation."""
        return self._data.get('abbreviation')
    
    @property
    def short_name(self):
        """Get conference short name."""
        return self._data.get('shortName')

class ConferenceList(BaseModelList):
    """List of Conference objects."""
    
    def __init__(self, data):
        """
        Initialize the conference list.
        
        Args:
            data (list): List of conference data from API
        """
        super().__init__(data, Conference)

class ConferenceMembership(BaseModel):
    """
    Conference membership model.
    
    Represents a team's membership in a conference for a specific season.
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
    def conference_id(self):
        """Get conference ID."""
        return self._data.get('conferenceId')
    
    @property
    def conference(self):
        """Get conference name."""
        return self._data.get('conference')
    
    @property
    def start_season(self):
        """Get start season."""
        return self._data.get('startSeason')
    
    @property
    def end_season(self):
        """Get end season."""
        return self._data.get('endSeason')

class ConferenceMembershipList(BaseModelList):
    """List of ConferenceMembership objects."""
    
    def __init__(self, data):
        """
        Initialize the conference membership list.
        
        Args:
            data (list): List of conference membership data from API
        """
        super().__init__(data, ConferenceMembership) 