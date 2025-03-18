"""
Direct test script to examine field names in the API response.

This script extracts data from the API and prints out the field names.
"""

import os
import sys
import json
from pprint import pprint
from dotenv import load_dotenv

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load environment variables
load_dotenv()

from cbbd import CBBDClient

def test_field_names():
    """Test the field names in the API response"""
    # Initialize client
    api_key = os.getenv("CBBD_API_KEY") or os.getenv("CFBD_API_KEY")
    client = CBBDClient(api_key=api_key)
    
    print("\n=== TESTING FIELD NAMES IN API RESPONSE ===")
    
    # Test conferences
    print("\n1. Testing Conference Fields")
    conferences = client.conferences.get_conferences()
    if conferences:
        print(f"Found {len(conferences)} conferences")
        conf = conferences[0]
        print(f"Conference fields: {dir(conf)}")
        print(f"Raw data: {conf._data}")
    
    # Test teams for 2025
    print("\n2. Testing Team Fields (2025)")
    teams_2025 = client.teams.get_teams(season=2025)
    if teams_2025:
        print(f"Found {len(teams_2025)} teams for 2025")
        team = teams_2025[0]
        print(f"Team fields: {dir(team)}")
        print(f"Raw data: {team._data}")
        print(f"Team.name: {team.name}, Team.conference: {team.conference}")
    
    # Test SEC teams for 2025
    print("\n3. Testing SEC Teams (2025)")
    sec_teams = client.teams.get_teams(conference="SEC", season=2025)
    print(f"Found {len(sec_teams)} SEC teams for 2025")
    for team in sec_teams:
        print(f"  {team.name}: conference = '{team.conference}'")
    
    # Test games for 2025
    print("\n4. Testing Game Fields (2025)")
    games_2025 = client.games.get_games(season=2025, team="Kentucky")
    if games_2025:
        print(f"Found {len(games_2025)} games for Kentucky in 2025")
        game = games_2025[0]
        print(f"Game fields: {dir(game)}")
        
        # Check specific fields
        fields_to_check = [
            "home_team", "homeTeam", 
            "away_team", "awayTeam",
            "home_conference", "homeConference", 
            "away_conference", "awayConference",
            "conference_game", "conferenceGame"
        ]
        
        print("\nChecking field access:")
        raw_data = game._data if hasattr(game, '_data') else game.__dict__
        print(f"Raw data keys: {list(raw_data.keys())}")
        
        for field in fields_to_check:
            try:
                value = getattr(game, field) if hasattr(game, field) else "Field not found"
                print(f"  {field}: {value}")
            except Exception as e:
                print(f"  {field}: Error - {str(e)}")

        # Check if conferenceGame exists and its value
        if hasattr(game, "conferenceGame") or "conferenceGame" in raw_data:
            print(f"\nconferenceGame value: {getattr(game, 'conferenceGame', raw_data.get('conferenceGame', 'Not found'))}")
        
        # Now test how to properly access these fields with correct casing
        print("\nAccessing with model properties:")
        try:
            print(f"  home_team via property: {game.home_team}")
            print(f"  away_team via property: {game.away_team}")
            print(f"  conference_game via property: {game.conference_game}")
        except Exception as e:
            print(f"  Error accessing properties: {str(e)}")
    
    # Test how the advanced API exposes the data
    print("\n5. Testing Advanced API (Conference Season)")
    profile = client.advanced.conference_season.get_profile(conference="SEC", season=2025)
    
    print(f"Profile keys: {list(profile.keys())}")
    
    # Check game format in the profile
    if "games" in profile and profile["games"]:
        print(f"Number of games in profile: {len(profile['games'])}")
        sample_game = profile["games"][0]
        print(f"Sample game fields in profile: {list(sample_game.keys())}")
        
        # Check how conference fields are named in the profile
        conference_fields = [key for key in sample_game.keys() if "conf" in key.lower()]
        print(f"Conference-related fields: {conference_fields}")

if __name__ == "__main__":
    test_field_names() 