"""
Substitutions API module for the CFBD Python SDK.

This module provides an API wrapper for substitution-related endpoints.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import Endpoints
from cbbd.utils.cache import cached
from cbbd.models.substitution import Substitution, SubstitutionList
from cbbd.api.base import BaseAPI


class SubstitutionsAPI(BaseAPI):
    """
    API wrapper for substitution-related endpoints.
    """
    
    def __init__(self, client):
        """
        Initialize the SubstitutionsAPI.
        
        Args:
            client: The CBBD client instance.
        """
        super().__init__(client)
    
    @cached
    def get_substitutions(
        self,
        game_id: Optional[int] = None,
        team: Optional[str] = None,
        player: Optional[str] = None
    ) -> SubstitutionList:
        """
        Get player substitutions.
        
        Args:
            game_id: Game ID filter
            team: Team name filter
            player: Player name filter
            
        Returns:
            A SubstitutionList object containing substitutions
        """
        params: Dict[str, Any] = {}
        
        if game_id is not None:
            params['gameId'] = game_id
            
        if team is not None:
            params['team'] = team
            
        if player is not None:
            params['player'] = player
            
        response = Endpoints.make_request(Endpoints.SUBSTITUTIONS, params)
        return SubstitutionList(response) 