# CBBD Python SDK Examples

This directory contains example scripts showcasing the usage of the CBBD Python SDK.

## Setup

1. Install the CBBD Python SDK:
   ```
   pip install cbbd-python-sdk
   ```

2. Create a `.env` file based on the `.env.example` file:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file and add your CBBD API key.

## Available Examples

- `basic_usage.py`: Demonstrates basic usage of the SDK, including querying teams, games, stats, rankings, and using advanced functionality.

## Running the Examples

Simply run the Python script:

```
python basic_usage.py
```

## Creating Your Own Examples

Feel free to modify these examples or create your own. The SDK provides a comprehensive set of APIs for accessing college basketball data.

Basic pattern for using the SDK:

```python
from cbbd import CBBDClient

# Initialize the client
client = CBBDClient(api_key="your-api-key")

# Use various API endpoints
teams = client.teams.get_teams()
games = client.games.get_games(team="Duke", season=2023)
stats = client.stats.get_team_stats(team="Duke", season=2023)

# Access advanced functionality
profile = client.advanced.team_season.get_profile(team="Duke", season=2023)
```

Refer to the SDK documentation for more details on available endpoints and parameters. 