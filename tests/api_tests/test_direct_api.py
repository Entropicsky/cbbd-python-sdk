"""
Direct API testing script.

This script makes direct API calls to test the raw responses.
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load environment variables
load_dotenv()

from cbbd import CBBDClient

def save_json(data, name):
    """Save data to a JSON file"""
    output_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved to {filepath}")

def test_teams_api(api_key=None, season=2023):
    """Test teams API"""
    client = CBBDClient(api_key=api_key or os.getenv("CBBD_API_KEY") or os.getenv("CFBD_API_KEY"))
    
    print(f"\n=== Testing Teams API for season {season} ===")
    
    # Get all teams
    print("\n1. Getting all teams")
    teams = client.teams.get_teams(season=season)
    print(f"Found {len(teams)} teams")
    
    if len(teams) > 0:
        # Check the first team
        team = teams[0]
        print(f"\nFirst team: {team.name} ({team.conference})")
        print(f"Team fields: {dir(team)}")
        
        # Print raw data for the first team
        if hasattr(team, '_data'):
            print(f"Raw data: {team._data}")
        else:
            print(f"Raw data: {team.__dict__}")
        
        # Save raw response
        raw_data = [t._data if hasattr(t, '_data') else t.__dict__ for t in teams]
        save_json(raw_data, f"teams_{season}")
    
    # Get teams by conference
    conferences_to_test = ["SEC", "ACC", "Big Ten", "Big 12", "Pac-12"]
    
    for conf in conferences_to_test:
        print(f"\n2. Getting teams for conference: {conf}")
        conf_teams = client.teams.get_teams(conference=conf, season=season)
        print(f"Found {len(conf_teams)} teams for {conf}")
        
        if len(conf_teams) > 0:
            team_names = [t.name for t in conf_teams]
            print(f"Teams: {team_names}")

def test_games_api(api_key=None, season=2023, team="Duke"):
    """Test games API"""
    client = CBBDClient(api_key=api_key or os.getenv("CBBD_API_KEY") or os.getenv("CFBD_API_KEY"))
    
    print(f"\n=== Testing Games API for season {season} ===")
    
    # Get all games
    print("\n1. Getting all games")
    games = client.games.get_games(season=season)
    print(f"Found {len(games)} games")
    
    if len(games) > 0:
        # Check the first game
        game = games[0]
        print(f"\nFirst game: {game.away_team} @ {game.home_team}")
        print(f"Game fields: {dir(game)}")
        
        # Save raw response
        raw_data = [g._data if hasattr(g, '_data') else g.__dict__ for g in games[:10]]  # Save first 10 games
        save_json(raw_data, f"games_{season}")
    
    # Get games by team
    print(f"\n2. Getting games for team: {team}")
    team_games = client.games.get_games(season=season, team=team)
    print(f"Found {len(team_games)} games for {team}")
    
    if len(team_games) > 0:
        opponents = [g.away_team if g.home_team == team else g.home_team for g in team_games]
        print(f"Opponents: {opponents}")
    
    # Get games by conference
    conferences_to_test = ["SEC", "ACC"]
    
    for conf in conferences_to_test:
        print(f"\n3. Getting games for conference: {conf}")
        conf_games = client.games.get_games(season=season, conference=conf)
        print(f"Found {len(conf_games)} games for {conf}")
        
        if len(conf_games) > 0 and len(conf_games) < 10:
            game_info = [(g.away_team, g.home_team, g.away_points, g.home_points) for g in conf_games]
            print(f"Games: {game_info}")

def test_conferences_api(api_key=None):
    """Test conferences API"""
    client = CBBDClient(api_key=api_key or os.getenv("CBBD_API_KEY") or os.getenv("CFBD_API_KEY"))
    
    print("\n=== Testing Conferences API ===")
    
    # Get all conferences
    print("\n1. Getting all conferences")
    conferences = client.conferences.get_conferences()
    print(f"Found {len(conferences)} conferences")
    
    if len(conferences) > 0:
        # Print all conferences
        conference_info = [(c.name, c.abbreviation) for c in conferences]
        print(f"Conferences: {conference_info}")
        
        # Save raw response
        raw_data = [c._data if hasattr(c, '_data') else c.__dict__ for c in conferences]
        save_json(raw_data, "conferences")
        
        # Test conference matching
        test_abbrs = ["SEC", "ACC", "Big Ten", "Big 12", "Pac-12"]
        for abbr in test_abbrs:
            print(f"\nLooking for conference with abbreviation: {abbr}")
            found = False
            for c in conferences:
                if c.abbreviation and c.abbreviation.lower() == abbr.lower():
                    print(f"Exact match found: {c.name} ({c.abbreviation})")
                    found = True
                    break
                elif c.name and abbr.lower() in c.name.lower():
                    print(f"Partial match found: {c.name} ({c.abbreviation})")
                    found = True
                    break
            
            if not found:
                print(f"No match found for {abbr}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test API endpoints directly")
    parser.add_argument("--season", type=int, default=2023, help="Season year")
    parser.add_argument("--api-key", type=str, help="API key (optional, will use env var if not provided)")
    parser.add_argument("--team", type=str, default="Duke", help="Team to test with")
    parser.add_argument("--endpoint", type=str, choices=["teams", "games", "conferences", "all"], 
                        default="all", help="Endpoint to test")
    
    args = parser.parse_args()
    
    if args.endpoint == "teams" or args.endpoint == "all":
        test_teams_api(api_key=args.api_key, season=args.season)
    
    if args.endpoint == "games" or args.endpoint == "all":
        test_games_api(api_key=args.api_key, season=args.season, team=args.team)
    
    if args.endpoint == "conferences" or args.endpoint == "all":
        test_conferences_api(api_key=args.api_key) 