"""
Advanced functionality for the CBBD Python SDK.

This module provides advanced functionality that combines multiple API endpoints
to provide more comprehensive data and analysis.
"""

from cbbd.advanced.team_season import TeamSeasonProfile
from cbbd.advanced.player_season import PlayerSeasonProfile
from cbbd.advanced.game_analysis import GameAnalysis
from cbbd.advanced.conference_season import ConferenceSeason


class AdvancedAPI:
    """
    Advanced functionality for the CBBD Python SDK.
    """
    
    def __init__(self, client):
        """
        Initialize the advanced functionality.
        
        Args:
            client (CBBDClient): Client instance for API communication
        """
        self.client = client
        self.team_season = TeamSeasonProfile(client)
        self.player_season = PlayerSeasonProfile(client)
        self.game_analysis = GameAnalysis(client)
        self.conference_season = ConferenceSeason(client) 