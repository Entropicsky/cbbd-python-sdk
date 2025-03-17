"""
Conferences API for the CFBD Python SDK.
"""

from ..constants import Endpoints
from ..utils.cache import cached
from ..models.conference import Conference, ConferenceList, ConferenceMembershipList
from .base import BaseAPI

class ConferencesAPI(BaseAPI):
    """API wrapper for conference-related endpoints."""
    
    @cached
    def get_conferences(self):
        """
        Get list of conferences.
        
        Returns:
            ConferenceList: List of Conference objects
        """
        data = self._request(Endpoints.CONFERENCES)
        return ConferenceList(data)
    
    @cached
    def get_conference_by_abbreviation(self, abbreviation):
        """
        Get conference by abbreviation.
        
        Args:
            abbreviation (str): Conference abbreviation
            
        Returns:
            Conference: Conference object or None if not found
        """
        conferences = self.get_conferences()
        for conference in conferences:
            if conference.abbreviation.lower() == abbreviation.lower():
                return conference
        return None
    
    @cached
    def get_conference_by_name(self, name):
        """
        Get conference by name.
        
        Args:
            name (str): Conference name
            
        Returns:
            Conference: Conference object or None if not found
        """
        conferences = self.get_conferences()
        for conference in conferences:
            if conference.name.lower() == name.lower() or conference.short_name.lower() == name.lower():
                return conference
        return None
    
    @cached
    def get_conference_history(self):
        """
        Get historical conference membership.
        
        Returns:
            ConferenceMembershipList: List of ConferenceMembership objects
        """
        data = self._request(Endpoints.CONFERENCES_HISTORY)
        return ConferenceMembershipList(data) 