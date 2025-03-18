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
- 🧪 Robust testing framework for API integration

## Recent Updates

- Added `ConferenceSeason` class for comprehensive conference season data
- Enhanced field handling for camelCase API responses
- Fixed conference game counting in the Streamlit app
- Added comprehensive test scripts for API data validation
- Implemented special handling for the SEC conference 2024-2025 seasons

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
    
# Get comprehensive conference season profile
conference_profile = client.advanced.conference_season.get_profile(
    conference="SEC",
    season=2023
)
print(f"Conference: {conference_profile['conference']['name']}")
print(f"Teams: {len(conference_profile['teams'])}")
print(f"Games: {len(conference_profile['games'])}")
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
- **Conference Season Profile**: Complete conference season data including games and standings

### Example: Conference Season Profile

```python
# Get comprehensive conference season profile
profile = client.advanced.conference_season.get_profile(
    conference="SEC",
    season=2025
)

# Access different aspects of the profile
print(f"Conference: {profile['conference']['name']}")
print(f"Teams: {len(profile['teams'])}")

# Count conference games
conference_games = [g for g in profile['games'] if g['conferenceGame'] == True]
print(f"Conference Games: {len(conference_games)}")

# View standings
for team in profile['standings'][:3]:
    print(f"{team['team']}: {team['conference_wins']}-{team['conference_losses']}")
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

## Testing Framework

The SDK includes a comprehensive testing framework to ensure reliability:

```
tests/
├── api_tests/             # Tests for API functionality
│   ├── test_conference_fields.py
│   ├── test_conference_season.py
│   ├── test_game_fields.py
│   └── test_sec_2025.py
└── streamlit/            # Tests for Streamlit integration
```

Run the tests with:

```bash
python -m tests.api_tests.test_game_fields
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
- Conference season visualization
- Data transformation examples
- API response inspection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [College Basketball Data API](https://api.collegebasketballdata.com/docs) for providing the data
- All contributors to this project 