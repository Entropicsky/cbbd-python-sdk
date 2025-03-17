"""
Rankings API module for the CBBD Python SDK.

This module provides an API wrapper for rankings-related endpoints.
"""

from typing import Dict, List, Optional, Any
import logging

from cbbd.constants import Endpoints, SeasonTypes
from cbbd.utils.cache import cached
from cbbd.utils.validation import validate_season
from cbbd.models.ranking import Ranking, RankingList
from .base import BaseAPI


class RankingsAPI(BaseAPI):
    """
    API wrapper for rankings-related endpoints.
    """
    
    @cached
    def get_rankings(
        self,
        season: int,
        week: Optional[int] = None,
        season_type: str = SeasonTypes.REGULAR,
        poll_type: Optional[str] = None
    ) -> RankingList:
        """
        Get team rankings.
        
        Args:
            season: The season year (e.g., 2021)
            week: Week filter
            season_type: Season type filter (regular or postseason)
            poll_type: Poll type filter (e.g., 'ap', 'coaches')
            
        Returns:
            A RankingList object containing rankings
        """
        params: Dict[str, Any] = {
            'season': validate_season(season),
            'seasonType': season_type
        }
        
        if week is not None:
            params['week'] = week
            
        if poll_type is not None:
            params['pollType'] = poll_type
        
        data = self._request(Endpoints.RANKINGS, params)
        
        # Debug the raw API response
        logging.info(f"Rankings API response: {data}")
        print(f"Raw rankings data: {data}")
        
        # If the response doesn't match the expected structure, adapt it
        # The API expects a list of rankings, each with a 'polls' field
        if data and isinstance(data, list) and len(data) > 0:
            # Check if the data matches expected structure
            if 'polls' not in data[0] and 'pollType' in data[0]:
                # The data seems to be a flattened structure
                # Group it by week to match our model
                adapted_data = []
                
                # Group by week
                weeks = {}
                for item in data:
                    week_num = item.get('week')
                    if week_num not in weeks:
                        weeks[week_num] = {
                            'season': item.get('season'),
                            'seasonType': item.get('seasonType'),
                            'week': week_num,
                            'polls': {}
                        }
                    
                    poll_type_val = item.get('pollType')
                    if poll_type_val not in weeks[week_num]['polls']:
                        weeks[week_num]['polls'][poll_type_val] = {
                            'poll': item.get('pollType'),  # Using pollType as poll name too
                            'pollType': poll_type_val,
                            'ranks': []
                        }
                    
                    # Add this team to the ranks for this poll
                    weeks[week_num]['polls'][poll_type_val]['ranks'].append({
                        'rank': item.get('ranking'),
                        'school': item.get('team'),
                        'conference': item.get('conference'),
                        'firstPlaceVotes': item.get('firstPlaceVotes'),
                        'points': item.get('points')
                    })
                
                # Convert the grouped data to the expected format
                for week_data in weeks.values():
                    week_data['polls'] = list(week_data['polls'].values())
                    adapted_data.append(week_data)
                
                return RankingList(adapted_data)
                
        return RankingList(data)
    
    @cached
    def get_poll_teams(
        self,
        season: int,
        week: Optional[int] = None,
        poll: Optional[str] = None,
        team: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get teams that were ranked in polls.
        
        Args:
            season: The season year (e.g., 2021)
            week: Week filter
            poll: Poll name filter (e.g., 'AP Top 25', 'Coaches Poll')
            team: Team name filter
            
        Returns:
            A list of dictionaries containing poll team data
        """
        params: Dict[str, Any] = {
            'season': validate_season(season)
        }
        
        if week is not None:
            params['week'] = week
            
        if poll is not None:
            params['poll'] = poll
            
        if team is not None:
            params['team'] = team
            
        return self._request(Endpoints.POLL_TEAMS, params) 