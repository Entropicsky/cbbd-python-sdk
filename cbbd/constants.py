"""
Constants for the CBBD Python SDK.
"""

# Base API URL
BASE_URL = "https://api.collegebasketballdata.com"

# API Endpoints
class Endpoints:
    """API endpoint constants."""
    
    # Games endpoints
    GAMES = "/games"
    GAMES_MEDIA = "/games/media"
    GAMES_TEAMS = "/games/teams"
    GAMES_PLAYERS = "/games/players"
    
    # Plays endpoints
    PLAYS_GAME = "/plays/game/{game_id}"
    PLAYS_PLAYER = "/plays/player/{player_id}"
    PLAYS_TEAM = "/plays/team"
    PLAYS_DATE = "/plays/date"
    PLAYS_TOURNAMENT = "/plays/tournament"
    PLAYS_TYPES = "/plays/types"
    
    # Teams endpoints
    TEAMS = "/teams"
    TEAMS_ROSTER = "/teams/roster"
    
    # Conferences endpoints
    CONFERENCES = "/conferences"
    CONFERENCES_HISTORY = "/conferences/history"
    
    # Venues endpoint
    VENUES = "/venues"
    
    # Stats endpoints
    STATS_TEAM_SEASON = "/stats/team/season"
    STATS_TEAM_SHOOTING_SEASON = "/stats/team/shooting/season"
    STATS_PLAYER_SEASON = "/stats/player/season"
    STATS_PLAYER_SHOOTING_SEASON = "/stats/player/shooting/season"
    
    # Rankings endpoint
    RANKINGS = "/rankings"
    
    # Ratings endpoints
    RATINGS_SRS = "/ratings/srs"
    RATINGS_ADJUSTED = "/ratings/adjusted"
    
    # Lines endpoints
    LINES = "/lines"
    LINES_PROVIDERS = "/lines/providers"
    
    # Lineups endpoints
    LINEUPS_TEAM = "/lineups/team"
    LINEUPS_GAME = "/lineups/game/{game_id}"
    
    # Draft endpoints
    DRAFT_TEAMS = "/draft/teams"
    DRAFT_POSITIONS = "/draft/positions"
    DRAFT_PICKS = "/draft/picks"
    
    # Recruiting endpoint
    RECRUITING_PLAYERS = "/recruiting/players"
    
    # Substitutions endpoints
    SUBSTITUTIONS_GAME = "/substitutions/game/{game_id}"
    SUBSTITUTIONS_PLAYER = "/substitutions/player/{player_id}"
    SUBSTITUTIONS_TEAM = "/substitutions/team"

# Season types
class SeasonTypes:
    """Season type constants."""
    REGULAR = "regular"
    POSTSEASON = "postseason"
    PRESEASON = "preseason"

# Default values
DEFAULT_CACHE_TTL = 300  # 5 minutes 