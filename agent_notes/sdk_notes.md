# CFBD College Basketball API Notes

## API Basics
- Base URL: https://api.collegebasketballdata.com/
- Requires API key for authentication as a Bearer token in the Authorization header
- Patreon subscription required to obtain an API key from CollegeFootballData.com website
- Rate limitation not explicitly documented, but recommended to stay under 1000 calls per minute

## API Endpoints and Response Structures

### Games
- `/games`: Get game information with filters
  - Returns detailed game data including scores, teams, venue, etc.
  - Supports filtering by team, conference, date range, season, etc.
  - Each game includes period points (scores by half or overtime)
  - Includes game status (scheduled, final, etc.)
  - Includes venue information
  
- `/games/media`: Get broadcast information for games
  - Returns broadcast/media information for games
  - Same filtering capabilities as `/games`
  
- `/games/teams`: Get team box score statistics
  - Returns detailed team statistics for games
  - Includes four factors, shooting stats, etc.
  
- `/games/players`: Get player box score statistics
  - Returns detailed player statistics for games
  - Includes minutes, points, rebounds, etc. for each player

### Plays
- `/plays/game/{gameId}`: Get all plays for a specific game
  - Returns detailed play-by-play data
  - Includes score, time, players involved, etc.
  
- `/plays/player/{playerId}`: Get all plays for a specific player and season
- `/plays/team`: Get all plays for a specific team and season
- `/plays/date`: Get all plays for a specific date
- `/plays/tournament`: Get all plays for a specific tournament and season
- `/plays/types`: Get list of play types

### Teams
- `/teams`: Get historical team information
  - Returns basic team data including name, conference, colors, etc.
  - Includes current venue information
  
- `/teams/roster`: Get team roster information
  - Returns player listings for a team in a specific season
  - Includes position, jersey number, height/weight, etc.

### Conferences
- `/conferences`: Get list of conferences
  - Returns basic conference data including name, abbreviation, etc.
  
- `/conferences/history`: Get historical conference membership
  - Returns historical data about conference members over time

### Venues
- `/venues`: Get venue information
  - Returns arena/venue data including name, location, etc.

### Stats
- `/stats/team/season`: Get team season statistics
  - Returns comprehensive team statistics for a season
  - Includes offensive and defensive metrics
  - Includes four factors, shooting percentages, etc.
  
- `/stats/team/shooting/season`: Get team season shooting statistics
  - Returns shooting-specific statistics
  - Breaks down shots by type (dunks, layups, jump shots, etc.)
  
- `/stats/player/season`: Get player season statistics
  - Returns comprehensive player statistics for a season
  - Includes advanced metrics like usage, offensive/defensive ratings
  - Includes shooting percentages by type
  
- `/stats/player/shooting/season`: Get player season shooting statistics
  - Returns shooting-specific statistics for players
  - Breaks down shots by type (dunks, layups, jump shots, etc.)

### Rankings
- `/rankings`: Get historical poll data
  - Returns historical rankings from polls (AP, Coaches)
  - Includes votes, points, etc.

### Ratings
- `/ratings/srs`: Get SRS ratings
  - Returns Simple Rating System ratings
  
- `/ratings/adjusted`: Get adjusted efficiency ratings
  - Returns efficiency metrics adjusted for competition

### Lines
- `/lines`: Get betting lines for games
  - Returns betting odds for games
  - Includes spread, over/under, moneyline
  
- `/lines/providers`: Get list of betting providers

### Lineups
- `/lineups/team`: Get lineup statistics for a team
  - Returns data on specific player combinations
  
- `/lineups/game/{gameId}`: Get lineup statistics for a game

### Draft
- `/draft/teams`: Get list of NBA teams
- `/draft/positions`: Get list of NBA positions
- `/draft/picks`: Get draft pick information

### Recruiting
- `/recruiting/players`: Get player recruiting information
  - Returns recruiting rankings and ratings

### Substitutions
- `/substitutions/game/{gameId}`: Get substitutions for a game
- `/substitutions/player/{playerId}`: Get substitutions for a player
- `/substitutions/team`: Get substitutions for a team

## Ideas for Advanced Combined Endpoints

### Team Season Profile
Combine:
- Team information
- Conference information
- Games schedule for the season
- Team season stats
- Team roster
- Rankings for the team that season

### Player Career Profile
Combine:
- Player basic information
- Player stats across multiple seasons
- Player game logs
- Shot charts if available
- Advanced metrics

### Game Detail
Combine:
- Game basic information
- Team box scores
- Player box scores
- Play-by-play data
- Media/broadcast information
- Betting lines

### Conference Dashboard
Combine:
- Conference information
- All teams in the conference
- Conference standings
- Conference stats leaders

## Authentication Implementation
- API key stored in environment variable
- Pass as Bearer token in Authorization header
- Example: `headers = {"Authorization": f"Bearer {API_KEY}"}`

## Error Handling Considerations
- Handle rate limiting errors (429)
- Handle authentication errors (401)
- Handle not found errors (404)
- Provide meaningful error messages

## Caching Strategies
- Cache relatively static data (teams, conferences, venues)
- Cache responses for a short time to reduce API calls
- Implement optional caching configurable by the user

## Testing Approaches
- Create unit tests for each endpoint wrapper
- Create integration tests for combined endpoints
- Use mock responses for unit tests
- Use actual API for integration tests (with rate limiting) 