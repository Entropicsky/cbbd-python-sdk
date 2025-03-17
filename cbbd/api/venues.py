"""
API endpoints for venue information.
"""
from typing import Optional, List, Dict, Any
import logging

from .base import BaseAPI
from ..models.venue import Venue  # This import might need adjustment based on existing models

logger = logging.getLogger(__name__)

class VenuesAPI(BaseAPI):
    """
    Client for venues API endpoints.
    """
    
    def __init__(self, client):
        """
        Initialize the VenuesAPI with a CBBDClient.
        
        Args:
            client: The CBBDClient instance to use for making requests.
        """
        super().__init__(client)
        
    def get_venues(self) -> List[Venue]:
        """
        Get a list of all venues.
        
        Returns:
            A list of Venue objects.
        """
        logger.info("Getting all venues")
        try:
            path = "/venues"
            return self._client.make_request(path) or []
        except Exception as e:
            logger.error(f"Error getting venues: {e}")
            return []
    
    def get_venue(self, venue_id: int) -> Optional[Venue]:
        """
        Get a specific venue by ID.
        
        Args:
            venue_id: The ID of the venue to get.
            
        Returns:
            A Venue object if found, None otherwise.
        """
        logger.info(f"Getting venue with ID {venue_id}")
        try:
            path = f"/venues/{venue_id}"
            return self._client.make_request(path)
        except Exception as e:
            logger.error(f"Error getting venue: {e}")
            return None 