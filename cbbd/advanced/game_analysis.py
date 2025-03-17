"""
Game analysis advanced functionality for the CBBD Python SDK.

This module provides advanced functionality for analyzing individual games.
"""

from typing import Dict, List, Optional, Any
from collections import defaultdict

from cbbd.utils.cache import cached


class GameAnalysis:
    """
    Advanced functionality for analyzing individual games.
    """
    
    def __init__(self, client):
        """
        Initialize the game analysis.
        
        Args:
            client (CBBDClient): Client instance for API communication
        """
        self.client = client
    
    @cached
    def get_game_analysis(
        self,
        game_id: int
    ) -> Dict[str, Any]:
        """
        Get a comprehensive analysis of a game.
        
        Args:
            game_id: Game ID
            
        Returns:
            A dictionary containing comprehensive game analysis
        """
        # Get game info
        game_info = self.client.games.get_game(game_id=game_id)
        
        # Get play-by-play data
        plays = self.client.plays.get_plays(game_id=game_id)
        
        # Get team stats
        team_stats = self.client.games.get_team_stats(game_id=game_id)
        
        # Get player stats
        player_stats = self.client.games.get_player_stats(game_id=game_id)
        
        # Get scoring plays
        scoring_plays = [play for play in plays if getattr(play, 'scoring_play', False)]
        
        # Get key plays (scoring plays, important moments)
        key_plays = [
            play for play in plays if (
                getattr(play, 'scoring_play', False) or 
                'turnover' in str(getattr(play, 'play_type', '')).lower()
            )
        ]
        
        # Analyze play distribution
        play_types = defaultdict(int)
        for play in plays:
            play_type = getattr(play, 'play_type', None)
            if play_type:
                play_types[play_type] += 1
        
        # Analyze player involvement
        player_involvement = defaultdict(int)
        for play in plays:
            if hasattr(play, 'to_dict'):
                play_dict = play.to_dict()
                for key, value in play_dict.items():
                    if 'player' in key and value:
                        player_involvement[value] += 1
        
        # Compile the analysis
        analysis = {
            'game': game_info.to_dict() if hasattr(game_info, 'to_dict') else {},
            'team_stats': [stat.to_dict() if hasattr(stat, 'to_dict') else stat for stat in team_stats] if team_stats else [],
            'player_stats': [stat.to_dict() if hasattr(stat, 'to_dict') else stat for stat in player_stats] if player_stats else [],
            'scoring_plays': [play.to_dict() if hasattr(play, 'to_dict') else play for play in scoring_plays],
            'key_plays': [play.to_dict() if hasattr(play, 'to_dict') else play for play in key_plays],
            'play_distribution': dict(play_types),
            'player_involvement': dict(player_involvement)
        }
        
        return analysis 