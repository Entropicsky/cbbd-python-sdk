"""
Team season profile advanced functionality for the CBBD Python SDK.

This module provides advanced functionality for getting comprehensive team season data.
"""

from typing import Dict, List, Optional, Any

from cbbd.constants import SeasonTypes
from cbbd.utils.cache import cached


class TeamSeasonProfile:
    """
    Advanced functionality for getting comprehensive team season data.
    """
    
    def __init__(self, client):
        """
        Initialize the team season profile.
        
        Args:
            client (CBBDClient): Client instance for API communication
        """
        self.client = client
    
    @cached
    def get_profile(
        self,
        team: str,
        season: int,
        season_type: str = SeasonTypes.REGULAR
    ) -> Dict[str, Any]:
        """
        Get a comprehensive profile of a team's season.
        
        Args:
            team: Team name
            season: Season year
            season_type: Season type (regular, postseason, or both)
            
        Returns:
            A dictionary containing comprehensive team season data
        """
        # Get team info - don't pass team parameter to get_teams, filter afterwards
        teams = self.client.teams.get_teams()
        team_info = next((t.to_dict() for t in teams if t.name == team), {})
        
        # Get team roster
        roster = self.client.teams.get_roster(team=team, season=season)
        
        # Get team games
        games = self.client.games.get_games(
            team=team,
            season=season,
            season_type=season_type
        )
        
        # Get team stats
        team_stats = self.client.stats.get_team_stats(
            team=team,
            season=season,
            season_type=season_type
        )
        
        # Get team rankings
        rankings = self.client.rankings.get_rankings(
            season=season,
            season_type=season_type
        )
        team_rankings = []
        for ranking in rankings:
            for poll in ranking.polls:
                for rank in poll.ranks:
                    if rank.school == team:
                        team_rankings.append({
                            'week': ranking.week,
                            'poll': poll.poll,
                            'rank': rank.rank
                        })
        
        # Get team ratings
        srs_ratings = self.client.ratings.get_srs_ratings(
            season=season,
            team=team
        )
        
        # Get adjusted efficiency ratings
        adjusted_ratings = self.client.ratings.get_adjusted_ratings(
            season=season,
            team=team
        )
        
        # Compile the profile
        profile = {
            'team': team_info,
            'roster': roster.to_dict() if hasattr(roster, 'to_dict') else {},
            'games': [game.to_dict() for game in games],
            'stats': [stat.to_dict() for stat in team_stats],
            'rankings': team_rankings,
            'ratings': {
                'srs': [rating.to_dict() for rating in srs_ratings],
                'adjusted': [rating.to_dict() for rating in adjusted_ratings]
            }
        }
        
        return profile 