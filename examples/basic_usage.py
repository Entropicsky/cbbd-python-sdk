#!/usr/bin/env python3
"""
Basic usage examples for the CBBD Python SDK.
"""

import os
import logging
from dotenv import load_dotenv
from cbbd import CBBDClient

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Initialize the client with your API key
    api_key = os.getenv("CBBD_API_KEY")
    if not api_key:
        raise ValueError("No API key found. Please set the CBBD_API_KEY environment variable.")
    
    client = CBBDClient(api_key=api_key)
    
    # Example 1: Get teams
    print("\n=== Teams Example ===")
    teams = client.teams.get_teams(conference="ACC")
    print(f"Found {len(teams)} teams in the ACC:")
    for team in teams:
        print(f"  - {team.name} ({team.mascot})")
    
    # Example 2: Get games for a specific team and season
    print("\n=== Games Example ===")
    team_name = "Duke"
    season = 2023
    games = client.games.get_games(team=team_name, season=season)
    print(f"Found {len(games)} games for {team_name} in {season}:")
    for game in games:
        result = ""
        if game.home_team == team_name:
            result = "W" if game.home_winner else "L"
            score = f"{game.home_points}-{game.away_points}"
            opponent = game.away_team
        else:
            result = "W" if game.away_winner else "L"
            score = f"{game.away_points}-{game.home_points}"
            opponent = game.home_team
        
        print(f"  - {result} vs {opponent}: {score}")
    
    # Example 3: Get team stats
    print("\n=== Team Stats Example ===")
    team_stats = client.stats.get_team_stats(team=team_name, season=season)
    if team_stats:
        stats = team_stats[0]  # Get the first stats object
        print(f"Stats for {team_name} ({season}):")
        print(f"  - Games: {stats.games}")
        print(f"  - Wins: {stats.wins}")
        print(f"  - Losses: {stats.losses}")
        print(f"  - Points: {stats.points.total} (avg: {stats.points.avg})")
        print(f"  - FG%: {stats.field_goals.pct:.1%}")
        print(f"  - 3PT%: {stats.three_point_field_goals.pct:.1%}")
        print(f"  - FT%: {stats.free_throws.pct:.1%}")
    
    # Example 4: Get player stats
    print("\n=== Player Stats Example ===")
    player_stats = client.stats.get_player_stats(team=team_name, season=season)
    print(f"Top 5 scorers for {team_name} ({season}):")
    # Sort by points and get top 5
    top_scorers = sorted(player_stats, key=lambda x: x.points, reverse=True)[:5]
    for i, player in enumerate(top_scorers, 1):
        print(f"  {i}. {player.name}: {player.points} pts, {player.games} games")
    
    # Example 5: Get team rankings
    print("\n=== Rankings Example ===")
    rankings = client.rankings.get_rankings(season=season)
    if rankings:
        # Get the most recent week's rankings
        most_recent = max(rankings, key=lambda x: x.week)
        print(f"Rankings for Week {most_recent.week} ({season}):")
        # Get AP Poll (or another poll if AP not available)
        ap_poll = next((poll for poll in most_recent.polls if poll.poll == "AP Top 25"), most_recent.polls[0])
        for i, rank in enumerate(ap_poll.ranks[:10], 1):
            print(f"  {i}. {rank.team} ({rank.conference})")
    
    # Example 6: Use advanced functionality
    print("\n=== Advanced API Example ===")
    team_profile = client.advanced.team_season.get_profile(team=team_name, season=season)
    if team_profile:
        print(f"Team Season Profile for {team_name} ({season}):")
        # Show some basic info
        if 'team' in team_profile:
            print(f"  - Conference: {team_profile['team'].get('conference', 'N/A')}")
        
        # Show stats summary
        if 'stats_summary' in team_profile:
            stats = team_profile['stats_summary']
            print(f"  - Record: {stats.get('wins', 0)}-{stats.get('losses', 0)}")
            print(f"  - Points per game: {stats.get('points_per_game', 0):.1f}")
            print(f"  - FG%: {stats.get('fg_pct', 0):.1%}")
            print(f"  - 3PT%: {stats.get('three_pt_pct', 0):.1%}")
        
        # Show number of games and ranks
        if 'games' in team_profile:
            print(f"  - Games played: {len(team_profile['games'])}")
        
        if 'rankings' in team_profile:
            print(f"  - Rankings tracked: {len(team_profile['rankings'])}")

if __name__ == "__main__":
    main() 