"""
Team and roster data transformers.

This module provides transformers for team and roster data, 
converting API responses to DataFrames and cleaning data.
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union

from .base import BaseTransformer

class TeamsTransformer(BaseTransformer):
    """Transformer for teams data from the API."""
    
    @staticmethod
    def to_dataframe(teams_data: Any) -> pd.DataFrame:
        """
        Convert teams data to a DataFrame.
        
        Args:
            teams_data: Teams data from the API
            
        Returns:
            DataFrame with teams data
        """
        if not teams_data:
            return pd.DataFrame()
            
        # Handle both list and single object
        teams_list = teams_data if isinstance(teams_data, list) else [teams_data]
        
        # Extract raw data if we have model objects
        processed_data = []
        for team in teams_list:
            if hasattr(team, 'get_raw_data'):
                processed_data.append(team.get_raw_data())
            elif hasattr(team, '_data'):
                processed_data.append(team._data)
            else:
                processed_data.append(team)
        
        # Convert to DataFrame
        df = pd.DataFrame(processed_data)
        
        # Clean NULL values
        for col in df.columns:
            df[col] = df[col].apply(BaseTransformer.clean_null_values)
            
        # Convert numeric columns
        numeric_cols = ['id', 'conferenceId', 'currentVenueId']
        df = BaseTransformer.safe_convert_to_numeric(df, numeric_cols)
        
        return df


class RosterTransformer(BaseTransformer):
    """Transformer for team roster data from the API."""
    
    @staticmethod
    def to_dataframe(roster_data: Any) -> pd.DataFrame:
        """
        Convert roster data to a DataFrame with player information.
        
        Args:
            roster_data: Roster data from the API
            
        Returns:
            DataFrame with player data
        """
        if not roster_data:
            return pd.DataFrame()
        
        # Extract raw data if we have a model object
        raw_data = None
        if hasattr(roster_data, 'get_raw_data'):
            raw_data = roster_data.get_raw_data()
        elif hasattr(roster_data, '_data'):
            raw_data = roster_data._data
        else:
            raw_data = roster_data
            
        # Handle the case where we get a team object with players array
        players_data = []
        
        # Check if we have a direct players list
        if hasattr(roster_data, 'players'):
            players_list = roster_data.players
            for player in players_list:
                if hasattr(player, 'get_raw_data'):
                    players_data.append(player.get_raw_data())
                elif hasattr(player, '_data'):
                    players_data.append(player._data)
                else:
                    players_data.append(player)
        # Check if we have a raw data dict with players key
        elif isinstance(raw_data, dict) and 'players' in raw_data:
            players_data = raw_data['players']
        # Otherwise assume we were given just the players list
        else:
            players_data = raw_data if isinstance(raw_data, list) else [raw_data]
            
        # If we still don't have player data, return empty DataFrame
        if not players_data:
            return pd.DataFrame()
            
        # Process each player into a flattened format
        processed_players = []
        for player in players_data:
            player_dict = {}
            
            # Basic player info
            player_dict['id'] = BaseTransformer.extract_nested_value(player, 'id')
            player_dict['source_id'] = BaseTransformer.extract_nested_value(player, 'sourceId')
            player_dict['name'] = BaseTransformer.extract_nested_value(player, 'name')
            player_dict['first_name'] = BaseTransformer.extract_nested_value(player, 'firstName')
            player_dict['last_name'] = BaseTransformer.extract_nested_value(player, 'lastName')
            player_dict['jersey'] = BaseTransformer.extract_nested_value(player, 'jersey')
            player_dict['position'] = BaseTransformer.extract_nested_value(player, 'position')
            player_dict['height'] = BaseTransformer.extract_nested_value(player, 'height')
            player_dict['weight'] = BaseTransformer.extract_nested_value(player, 'weight')
            player_dict['year'] = BaseTransformer.extract_nested_value(player, 'year')
            player_dict['start_season'] = BaseTransformer.extract_nested_value(player, 'startSeason')
            player_dict['end_season'] = BaseTransformer.extract_nested_value(player, 'endSeason')
            
            # Extract hometown info
            hometown = BaseTransformer.extract_nested_value(player, 'hometown', {})
            player_dict['city'] = BaseTransformer.extract_nested_value(hometown, 'city')
            player_dict['state'] = BaseTransformer.extract_nested_value(hometown, 'state')
            player_dict['country'] = BaseTransformer.extract_nested_value(hometown, 'country')
            player_dict['latitude'] = BaseTransformer.extract_nested_value(hometown, 'latitude')
            player_dict['longitude'] = BaseTransformer.extract_nested_value(hometown, 'longitude')
            player_dict['county_fips'] = BaseTransformer.extract_nested_value(hometown, 'countyFips')
            
            # Alternate sources of hometown data
            if not player_dict['state'] and BaseTransformer.extract_nested_value(player, 'home_state'):
                player_dict['state'] = BaseTransformer.extract_nested_value(player, 'home_state')
                
            if not player_dict['country'] and BaseTransformer.extract_nested_value(player, 'home_country'):
                player_dict['country'] = BaseTransformer.extract_nested_value(player, 'home_country')
                
            # Add team info from the roster object if available
            if isinstance(raw_data, dict):
                player_dict['team'] = BaseTransformer.extract_nested_value(raw_data, 'team')
                player_dict['team_id'] = BaseTransformer.extract_nested_value(raw_data, 'teamId')
                player_dict['conference'] = BaseTransformer.extract_nested_value(raw_data, 'conference')
                player_dict['season'] = BaseTransformer.extract_nested_value(raw_data, 'season')
                
            processed_players.append(player_dict)
            
        # Convert to DataFrame
        df = pd.DataFrame(processed_players)
        
        # Calculate experience if start_season is available
        if 'start_season' in df.columns and 'season' in df.columns:
            df['experience'] = df.apply(
                lambda row: row['season'] - row['start_season'] if pd.notna(row['start_season']) else 0, 
                axis=1
            )
            
        # Build hometown string
        def build_hometown(row):
            city = row.get('city', '')
            state = row.get('state', '')
            country = row.get('country', '')
            
            # Filter out NULL and empty values
            if isinstance(city, str) and city.upper() == 'NULL':
                city = ''
            if isinstance(state, str) and state.upper() == 'NULL':
                state = ''
            if isinstance(country, str) and country.upper() == 'NULL':
                country = ''
                
            # Build the string based on available data
            if city and (state or country):
                location = state if state else country
                return f"{city}, {location}"
            elif city:
                return city
            elif state:
                return state
            elif country:
                return country
            else:
                return ""
                
        df['hometown'] = df.apply(build_hometown, axis=1)
        
        # Clean up and convert data types
        numeric_cols = ['id', 'height', 'weight', 'latitude', 'longitude', 
                       'start_season', 'end_season', 'team_id', 'season']
        df = BaseTransformer.safe_convert_to_numeric(df, numeric_cols)
        
        return df 