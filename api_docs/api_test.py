#!/usr/bin/env python3
"""
Test script for the College Basketball Data API
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('CFBD_API_KEY')

if not API_KEY:
    raise ValueError("API_KEY not found in .env file")

# Base URL for the API
BASE_URL = "https://api.collegebasketballdata.com"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json"
}

def make_request(endpoint, params=None):
    """Make a request to the API with the given endpoint and parameters"""
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params)
    
    # Check if the request was successful
    response.raise_for_status()
    
    return response.json()

def save_response(endpoint, data, params=None):
    """Save the API response to a file for reference"""
    # Create a friendly filename from the endpoint and parameters
    filename = endpoint.replace("/", "_").strip("_")
    if params:
        param_str = "_".join([f"{k}-{v}" for k, v in params.items() if v])
        filename = f"{filename}_{param_str}"
    
    # Save the response to a file
    with open(f"api_docs/responses/{filename}.json", "w") as f:
        json.dump(data, f, indent=2)

def test_endpoints():
    """Test various endpoints and save the responses"""
    
    # Create directory for responses if it doesn't exist
    os.makedirs("api_docs/responses", exist_ok=True)
    
    # Test 1: Get teams information
    try:
        print("Testing teams endpoint...")
        teams_data = make_request("/teams")
        save_response("/teams", teams_data)
        print(f"Found {len(teams_data)} teams")
    except Exception as e:
        print(f"Error with teams endpoint: {e}")
    
    # Test 2: Get conferences information
    try:
        print("Testing conferences endpoint...")
        conferences_data = make_request("/conferences")
        save_response("/conferences", conferences_data)
        print(f"Found {len(conferences_data)} conferences")
    except Exception as e:
        print(f"Error with conferences endpoint: {e}")
    
    # Test 3: Get games for a specific team and season
    try:
        print("Testing games endpoint with team filter...")
        params = {"team": "Duke", "season": 2023}
        games_data = make_request("/games", params)
        save_response("/games", games_data, params)
        print(f"Found {len(games_data)} games for Duke in 2023")
    except Exception as e:
        print(f"Error with games endpoint: {e}")
    
    # Test 4: Get team stats for a season
    try:
        print("Testing team stats endpoint...")
        params = {"season": 2023}
        team_stats_data = make_request("/stats/team/season", params)
        save_response("/stats/team/season", team_stats_data, params)
        print(f"Found {len(team_stats_data)} team stats records for 2023")
    except Exception as e:
        print(f"Error with team stats endpoint: {e}")
    
    # Test 5: Get player stats for a team and season
    try:
        print("Testing player stats endpoint...")
        params = {"team": "Duke", "season": 2023}
        player_stats_data = make_request("/stats/player/season", params)
        save_response("/stats/player/season", player_stats_data, params)
        if player_stats_data:
            print(f"Found {len(player_stats_data)} player stats records for Duke in 2023")
        else:
            print("No player stats found")
    except Exception as e:
        print(f"Error with player stats endpoint: {e}")

if __name__ == "__main__":
    test_endpoints() 