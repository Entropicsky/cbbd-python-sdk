"""
Example script demonstrating how to use data transformers in the CBBD SDK.

This example shows how to convert different API response objects
into pandas DataFrames for easier data analysis and visualization.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from cbbd import CBBDClient
from cbbd.transformers import RosterTransformer, RankingsTransformer, LinesTransformer

# Load API key from environment
load_dotenv()
api_key = os.getenv("CBBD_API_KEY")

def main():
    """Run the transformers example."""
    # Create the client
    client = CBBDClient(api_key=api_key)
    
    print("CBBD Transformers Example")
    print("========================\n")
    
    # Example 1: Transform team roster data
    print("\n1. Team Roster Example")
    print("--------------------")
    
    # Get Duke's roster for 2023
    roster = client.teams.get_roster(team="Duke", season=2023)
    
    # Convert to DataFrame using the client's transformers
    roster_df = client.transformers.roster_to_dataframe(roster)
    
    # Show the data
    print(f"Duke 2023 Roster: {len(roster_df)} players")
    print(roster_df[['name', 'position', 'jersey', 'height', 'weight', 'hometown']].head())
    
    # Calculate average height and weight by position
    position_stats = roster_df.groupby('position').agg({
        'height': 'mean',
        'weight': 'mean'
    }).reset_index()
    
    print("\nAverage Height and Weight by Position:")
    print(position_stats)
    
    # Example 2: Transform rankings data
    print("\n\n2. Rankings Example")
    print("-----------------")
    
    # Get AP Top 25 rankings for the 2023 season
    rankings = client.rankings.get_rankings(season=2023)
    
    # Convert to DataFrame
    rankings_df = RankingsTransformer.to_dataframe(rankings)
    
    # Filter to AP poll and get the top 10 from a specific poll
    ap_rankings = rankings_df[rankings_df['poll'] == 'AP Top 25'].sort_values('rank').head(10)
    
    print("AP Top 10 for 2023 Season:")
    print(ap_rankings[['rank', 'school', 'conference']].head(10))
    
    # Example 3: Transform betting lines data
    print("\n\n3. Betting Lines Example")
    print("----------------------")
    
    # Get betting lines for a specific team and season
    try:
        lines = client.lines.get_lines(team="Duke", season=2023)
        
        # Convert to DataFrame
        lines_df = client.transformers.lines_to_dataframe(lines)
        
        # Show the spread distribution
        print(f"Duke 2023 Betting Lines: {len(lines_df)} games")
        print("\nSpread Distribution:")
        spread_stats = lines_df['spread'].describe()
        print(spread_stats)
        
        # Filter to only games where Duke is the home team
        home_games = lines_df[lines_df['home_team'] == 'Duke']
        print(f"\nDuke Home Games: {len(home_games)}")
        print(home_games[['away_team', 'spread', 'over_under']].head())
        
    except Exception as e:
        print(f"Error fetching betting lines: {e}")
    
    # Example 4: Combine transformers with utilities
    print("\n\n4. DataFrame Utilities Example")
    print("----------------------------")
    
    # Get player stats for a team
    try:
        player_stats = client.stats.get_player_stats(team="Duke", season=2023)
        
        # Convert to DataFrame
        stats_df = client.transformers.player_stats_to_dataframe(player_stats)
        
        # Use the utils class to make the DataFrame visualization-ready
        numeric_cols = [
            'games', 'minutes', 'field_goals_made', 'field_goals_attempted',
            'three_point_made', 'three_point_attempted', 'free_throws_made',
            'free_throws_attempted', 'offensive_rebounds', 'defensive_rebounds',
            'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'fouls', 'points'
        ]
        
        categorical_cols = ['player', 'team', 'position']
        
        # Use the DataFrame utilities
        viz_df = client.transformers.utils.make_visualization_ready(
            stats_df,
            numeric_columns=numeric_cols,
            categorical_columns=categorical_cols
        )
        
        # Calculate per-game stats
        calculations = {
            'points_per_game': lambda df: df['points'] / df['games'],
            'rebounds_per_game': lambda df: df['rebounds'] / df['games'],
            'assists_per_game': lambda df: df['assists'] / df['games']
        }
        
        viz_df = client.transformers.utils.add_calculated_columns(viz_df, calculations)
        
        print("Duke 2023 Player Stats with Added Calculations:")
        print(viz_df[['player', 'games', 'points_per_game', 'rebounds_per_game', 'assists_per_game']].head())
        
    except Exception as e:
        print(f"Error fetching player stats: {e}")

if __name__ == "__main__":
    main() 