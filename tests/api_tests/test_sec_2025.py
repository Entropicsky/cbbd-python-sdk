"""
Test script specifically for SEC conference in 2025 season.
"""
import os
import sys
import logging
from dotenv import load_dotenv
from pprint import pprint

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to sys.path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load environment variables from .env file
load_dotenv()

from cbbd.client import CBBDClient

def test_sec_2025():
    """Test the SEC conference data for 2025 season."""
    logger.info("Starting SEC 2025 test")
    
    # Initialize the client with API key from environment
    api_key = os.getenv('CBBD_API_KEY') or os.getenv('CFBD_API_KEY')
    if not api_key:
        logger.error("No API key found in environment variables. Set CBBD_API_KEY or CFBD_API_KEY.")
        return
    
    logger.info(f"Using API key: {api_key[:5]}..." if api_key else "No API key found")
    client = CBBDClient(api_key=api_key)
    
    # Get conference profile
    logger.info("Getting SEC conference profile for 2025")
    try:
        conference_season = client.advanced.conference_season
        profile = conference_season.get_profile('SEC', 2025)
        
        # Log profile information
        logger.info(f"Profile keys: {list(profile.keys())}")
        logger.info(f"Conference: {profile['conference']}")
        logger.info(f"Number of teams: {len(profile['teams'])}")
        
        # List all teams
        logger.info("SEC Teams for 2025:")
        for i, team in enumerate(profile['teams']):
            team_name = team.get('name') or team.get('school')
            logger.info(f"  {i+1}. {team_name}")
        
        # Check games
        logger.info(f"Number of games: {len(profile['games'])}")
        if profile['games']:
            logger.info("Sample game fields:")
            sample_game = profile['games'][0]
            logger.info(f"Game keys: {list(sample_game.keys())}")
            
            # Check for conference games specifically
            conf_games = [g for g in profile['games'] if g.get('conferenceGame') == True]
            logger.info(f"Number of conference games: {len(conf_games)}")
            
            # Analyze a conference game
            if conf_games:
                logger.info("Sample conference game:")
                conf_game = conf_games[0]
                home_team = conf_game.get('homeTeam')
                away_team = conf_game.get('awayTeam')
                logger.info(f"  {away_team} @ {home_team}")
                logger.info(f"  Home conference: {conf_game.get('homeConference')}")
                logger.info(f"  Away conference: {conf_game.get('awayConference')}")
        
        # Check standings
        logger.info(f"Number of standings entries: {len(profile['standings'])}")
        if profile['standings']:
            logger.info("Top 3 teams in standings:")
            for i, standing in enumerate(profile['standings'][:3]):
                logger.info(f"  {i+1}. {standing['team']} ({standing['conference_wins']}-{standing['conference_losses']})")
        
    except Exception as e:
        logger.error(f"Error getting SEC profile for 2025: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    logger.info("SEC 2025 test completed")

if __name__ == "__main__":
    test_sec_2025() 