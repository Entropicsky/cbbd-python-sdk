"""
Player season profile advanced functionality for the CBBD Python SDK.

This module provides advanced functionality for getting comprehensive player season data.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import SeasonTypes
from cbbd.utils.cache import cached


class PlayerSeasonProfile:
    """
    Advanced functionality for getting comprehensive player season data.
    """
    
    def __init__(self, client):
        """
        Initialize the player season profile.
        
        Args:
            client (CBBDClient): Client instance for API communication
        """
        self.client = client
    
    @cached
    def get_profile(
        self,
        player_id: int,
        season: int,
        season_type: str = SeasonTypes.REGULAR
    ) -> Dict[str, Any]:
        """
        Get a comprehensive profile of a player's season.
        
        Args:
            player_id: Player ID
            season: Season year
            season_type: Season type (regular, postseason, or both)
            
        Returns:
            A dictionary containing comprehensive player season data
        """
        # Get player info
        player_info = {}
        
        # Get player stats
        player_stats = self.client.stats.get_player_season_stats(
            player_id=player_id,
            season=season,
            season_type=season_type
        )
        
        # Get player game stats
        player_game_stats = self.client.stats.get_player_game_stats(
            player_id=player_id,
            season=season,
            season_type=season_type
        )
        
        # Get player's team
        team = None
        if player_game_stats:
            team = player_game_stats[0].team
        
        # Get team games if we have a team
        team_games = []
        if team:
            team_games = self.client.games.get_games(
                team=team,
                season=season,
                season_type=season_type
            )
        
        # Get player's PBP data if available
        player_plays = []
        if team and team_games:
            for game in team_games:
                plays = self.client.plays.get_plays(
                    game_id=game.id
                )
                # Filter plays involving this player
                for play in plays:
                    if str(player_id) in str(play.to_dict()):
                        player_plays.append(play.to_dict())
        
        # Compile the profile
        profile = {
            'player_id': player_id,
            'season': season,
            'team': team,
            'season_stats': [stat.to_dict() for stat in player_stats],
            'game_stats': [stat.to_dict() for stat in player_game_stats],
            'plays': player_plays
        }
        
        return profile 