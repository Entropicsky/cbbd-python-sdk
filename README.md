# CBBD Python SDK

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/entropicsky/cbbd-python-sdk)](https://github.com/entropicsky/cbbd-python-sdk/blob/main/LICENSE)

A Python Software Development Kit (SDK) for the [College Basketball Data (CBBD) API](https://api.collegebasketballdata.com/docs). This SDK provides a structured, well-documented, and easy-to-use interface for accessing college basketball data.

## Features

- 🏀 Comprehensive API coverage for college basketball data
- 🔄 Automatic request retries and error handling
- 📦 Simple object-oriented interface with type hints
- 📊 Advanced functionality for data analysis and visualization
- 📝 Detailed logging for debugging
- 🔒 Proper authentication handling
- 💾 Caching support to reduce API calls
- 🔧 Data transformation utilities for pandas integration

## Installation

```bash
pip install cbbd-python-sdk
```

## Quick Start

```python
from cbbd import CBBDClient

# Initialize client with your API key
client = CBBDClient(api_key="your-api-key")

# Get team information
teams = client.teams.get_teams()
for team in teams:
    print(f"{team.name} ({team.conference})")

# Get games for a specific team and season
games = client.games.get_games(team="Duke", season=2023)
for game in games:
    print(f"{game.away_team} @ {game.home_team}: {game.away_points}-{game.home_points}")
```

## Authentication

To use this SDK, you'll need an API key from the CBBD API. You can get one by creating an account at [collegebasketballdata.com](https://collegebasketballdata.com).

Set your API key in one of two ways:

1. Pass it directly to the client:
   ```python
   client = CBBDClient(api_key="your-api-key")
   ```

2. Use environment variables (recommended):
   ```
   # .env file
   CBBD_API_KEY=your-api-key
   ```
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   
   client = CBBDClient()  # Will load from CBBD_API_KEY environment variable
   ```

## Available APIs

The SDK provides access to the following endpoints:

- **Teams API**: Team information and rosters
- **Games API**: Game schedules, results, and details
- **Conferences API**: Conference information and membership
- **Venues API**: Venue details
- **Stats API**: Team and player statistics
- **Rankings API**: Team rankings from various polls
- **Ratings API**: Team ratings from different rating systems
- **Plays API**: Play-by-play data
- **Lines API**: Betting lines and odds
- **Lineups API**: Team lineup combinations and statistics
- **Draft API**: NBA draft information
- **Recruiting API**: Recruiting data and team rankings
- **Substitutions API**: Player substitution data

## Advanced Functionality

The SDK also provides advanced functionality that combines multiple API endpoints:

- **Team Season Profile**: Comprehensive team season data
- **Player Season Profile**: Comprehensive player season data
- **Game Analysis**: Detailed game analysis

### Example: Team Season Profile

```python
# Get comprehensive team season profile
profile = client.advanced.team_season.get_profile(
    team="Duke",
    season=2023
)

# Access different aspects of the profile
print(f"Team: {profile['team']['name']}")
print(f"Record: {len([g for g in profile['games'] if g['home_winner'] or g['away_winner']])}-{len(profile['games']) - len([g for g in profile['games'] if g['home_winner'] or g['away_winner']])}")
print(f"Average Points: {sum(stat['points'] for stat in profile['stats']) / len(profile['stats']):.1f}")
```

## Data Transformation Utilities

The SDK includes data transformation utilities that make it easy to convert API responses into pandas DataFrames for analysis and visualization:

```python
# Get roster data
roster = client.teams.get_roster(team="Duke", season=2023)

# Convert to DataFrame
roster_df = client.transformers.roster_to_dataframe(roster)

# Analyze the data with pandas
avg_height_by_position = roster_df.groupby('position')['height'].mean()
print(avg_height_by_position)

# Create visualization-ready data
import matplotlib.pyplot as plt
avg_height_by_position.plot(kind='bar')
plt.title('Average Height by Position')
plt.show()
```

### Available Transformers

- `teams_to_dataframe()`: Convert team data to DataFrame
- `roster_to_dataframe()`: Convert roster data to DataFrame
- `games_to_dataframe()`: Convert games data to DataFrame
- `player_stats_to_dataframe()`: Convert player statistics to DataFrame
- `rankings_to_dataframe()`: Convert rankings data to DataFrame
- `ratings_to_dataframe()`: Convert ratings data to DataFrame
- `lines_to_dataframe()`: Convert betting lines data to DataFrame
- `plays_to_dataframe()`: Convert play-by-play data to DataFrame

### DataFrame Utilities

```python
# Make DataFrame visualization-ready
viz_df = client.transformers.utils.make_visualization_ready(
    df,
    numeric_columns=['points', 'rebounds', 'assists'],
    categorical_columns=['position', 'team']
)

# Add calculated columns
df_with_calcs = client.transformers.utils.add_calculated_columns(
    viz_df,
    {
        'points_per_game': lambda df: df['points'] / df['games'],
        'efficiency': lambda df: (df['points'] + df['rebounds'] + df['assists']) / df['minutes']
    }
)
```

## Caching

The SDK supports caching to reduce API calls:

```python
# Initialize client with custom cache TTL (time-to-live)
client = CBBDClient(use_cache=True, cache_ttl=600)  # 10 minutes
```

## Logging

Configure logging to help with debugging:

```python
import logging
from cbbd import CBBDClient

# Initialize client with custom logging
client = CBBDClient(
    log_level=logging.DEBUG,
    log_file="cbbd.log"
)
```

## Error Handling

The SDK provides specific exception types for different errors:

```python
from cbbd import CBBDClient
from cbbd.exceptions import CBBDAuthError, CBBDRateLimitError, CBBDNotFoundError

try:
    client = CBBDClient(api_key="invalid-api-key")
    teams = client.teams.get_teams()
except CBBDAuthError:
    print("Authentication failed. Check your API key.")
except CBBDRateLimitError:
    print("Rate limit exceeded. Please wait before making more requests.")
except CBBDNotFoundError:
    print("Resource not found.")
```

## Demo App

A Streamlit demo application is included to showcase the SDK's capabilities. To run it:

```bash
cd streamlit_app
streamlit run app.py
```

The demo app provides interactive examples of all the SDK's features, including:
- Team and player data visualization
- Game analysis
- Statistical comparisons
- Data transformation examples
- API response inspection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [College Basketball Data API](https://api.collegebasketballdata.com/docs) for providing the data
- All contributors to this project 