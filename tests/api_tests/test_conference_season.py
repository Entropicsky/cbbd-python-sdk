"""
Test script for ConferenceSeason advanced API functionality.
"""
import os
import sys
import logging
from dotenv import load_dotenv
from pprint import pprint

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to sys.path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load environment variables from .env file
load_dotenv()

from cbbd.client import CBBDClient

def get_team_name(team):
    """
    Safely get the name/school of a team, handling different object types.
    """
    if hasattr(team, 'name'):
        return team.name
    elif hasattr(team, 'school'):
        return team.school
    elif isinstance(team, dict):
        return team.get('name') or team.get('school') or "(unknown)"
    else:
        return str(team)

def get_team_conference_id(team):
    """
    Safely get the conference ID of a team, handling different object types.
    """
    if hasattr(team, 'conference'):
        conf = team.conference
        if hasattr(conf, 'id'):
            return conf.id
        elif isinstance(conf, dict) and 'id' in conf:
            return conf['id']
        elif isinstance(conf, str) and conf.isdigit():
            return int(conf)
    
    if hasattr(team, 'conference_id'):
        return team.conference_id
    
    if isinstance(team, dict):
        if 'conference' in team:
            conf = team['conference']
            if isinstance(conf, dict) and 'id' in conf:
                return conf['id']
            elif isinstance(conf, str) and conf.isdigit():
                return int(conf)
        if 'conferenceId' in team:
            return team['conferenceId']
    
    return None

def test_conference_season():
    """Test the ConferenceSeason functionality with detailed logging."""
    logger.info("Starting ConferenceSeason test")
    
    # Initialize the client with API key from environment
    api_key = os.getenv('CBBD_API_KEY') or os.getenv('CFBD_API_KEY')
    if not api_key:
        logger.error("No API key found in environment variables. Set CBBD_API_KEY or CFBD_API_KEY.")
        return
    
    logger.info(f"Using API key: {api_key[:5]}..." if api_key else "No API key found")
    client = CBBDClient(api_key=api_key)
    
    # Test ConferenceSeason initialization
    logger.info("Testing ConferenceSeason initialization")
    try:
        conference_season = client.advanced.conference_season
        logger.info("ConferenceSeason initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing ConferenceSeason: {str(e)}")
        return
    
    # Test get_conferences to understand the conference data format
    logger.info("Testing get_conferences to understand data format")
    try:
        conferences = client.conferences.get_conferences()
        logger.info(f"Retrieved {len(conferences)} conferences")
        
        # Log the first conference to see its structure
        if conferences:
            logger.info("First conference data structure:")
            first_conf = conferences[0]
            if hasattr(first_conf, '__dict__'):
                logger.info(f"Conference is an object with attributes: {dir(first_conf)}")
                logger.info(f"Conference __dict__: {first_conf.__dict__}")
                logger.info(f"Raw data from to_dict(): {first_conf.to_dict()}")
            else:
                logger.info(f"Conference is a dictionary: {first_conf}")
                
        # Get SEC conference for later reference
        sec_conf = None
        for conf in conferences:
            if hasattr(conf, 'abbreviation') and conf.abbreviation == 'SEC':
                sec_conf = conf
                logger.info(f"Found SEC conference: {conf.to_dict()}")
                break
    except Exception as e:
        logger.error(f"Error getting conferences: {str(e)}")
    
    # Test get_teams to understand team data format
    logger.info("Testing get_teams to understand data format")
    try:
        teams = client.teams.get_teams(season=2023)
        logger.info(f"Retrieved {len(teams)} teams for 2023")
        
        # Log the first team to see its structure
        if teams:
            logger.info("First team data structure:")
            first_team = teams[0]
            if hasattr(first_team, '__dict__'):
                logger.info(f"Team is an object with attributes: {dir(first_team)}")
                logger.info(f"Team __dict__: {first_team.__dict__}")
                logger.info(f"Raw data from to_dict(): {first_team.to_dict()}")
            else:
                logger.info(f"Team is a dictionary: {first_team}")
                
        # Check the actual field for the team name
        team_name_field = None
        if hasattr(first_team, 'name'):
            team_name_field = 'name'
            logger.info(f"Team name field is 'name': {first_team.name}")
        elif hasattr(first_team, 'school'):
            team_name_field = 'school'
            logger.info(f"Team name field is 'school': {first_team.school}")
        else:
            logger.info(f"Could not determine team name field. Available fields: {dir(first_team)}")
            
        # Check conference ID mapping directly
        sec_teams = []
        logger.info("Looking for SEC teams directly:")
        sec_id = 24  # SEC conference ID
        
        for team in teams:
            conf_id = get_team_conference_id(team)
            team_name = get_team_name(team)
            
            if conf_id == sec_id:
                sec_teams.append(team_name)
                logger.info(f"Found SEC team: {team_name}")
                
        logger.info(f"Found {len(sec_teams)} SEC teams by direct identification: {sec_teams}")
        
        # Try calling get_teams with a conference parameter
        try:
            logger.info("Testing get_teams with conference parameter")
            conf_teams = client.teams.get_teams(conference='SEC', season=2023)
            logger.info(f"Retrieved {len(conf_teams)} SEC teams using conference parameter")
            
            if conf_teams:
                logger.info(f"SEC teams using conference parameter: {[get_team_name(team) for team in conf_teams]}")
        except Exception as e:
            logger.error(f"Error getting teams with conference parameter: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting teams: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Test the arguments expected by get_teams method
    logger.info("Testing get_teams method signature")
    try:
        import inspect
        teams_signature = inspect.signature(client.teams.get_teams)
        logger.info(f"get_teams signature: {teams_signature}")
        logger.info(f"Parameter names: {list(teams_signature.parameters.keys())}")
    except Exception as e:
        logger.error(f"Error inspecting get_teams: {str(e)}")
    
    # Debug how conference filtering works in our codebase
    logger.info("Checking our conference team filtering logic:")
    try:
        for i, team in enumerate(teams[:20]):  # Look at first 20 teams
            team_name = get_team_name(team)
            logger.info(f"Team {i+1}: {team_name}")
            
            if hasattr(team, 'conference'):
                conf = team.conference
                if hasattr(conf, 'id'):
                    logger.info(f"  conference.id = {conf.id}")
                elif isinstance(conf, str):
                    logger.info(f"  conference = '{conf}'")
                elif isinstance(conf, dict):
                    logger.info(f"  conference dict: {conf}")
                else:
                    logger.info(f"  unknown conference type: {type(conf)}")
            
            if hasattr(team, 'conference_id'):
                logger.info(f"  conference_id = {team.conference_id}")
            
            # Check for dictionary format
            if isinstance(team, dict):
                if 'conference' in team:
                    conf = team.get('conference')
                    if isinstance(conf, dict):
                        logger.info(f"  conference dict: {conf}")
                    else:
                        logger.info(f"  conference = '{conf}'")
                if 'conferenceId' in team:
                    logger.info(f"  conferenceId = {team.get('conferenceId')}")
    except Exception as e:
        logger.error(f"Error examining team conference data: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Test the conference_season.get_profile method for a known conference
    test_conferences = [
        {"name": "SEC", "season": 2023},
        {"name": "Big Ten", "season": 2023},
        {"name": "A-10", "season": 2023},  # Atlantic 10
    ]
    
    for conf_data in test_conferences:
        conf_name = conf_data["name"]
        season = conf_data["season"]
        logger.info(f"Testing get_profile for {conf_name} in {season}")
        
        try:
            logger.info(f"Calling conference_season.get_profile({conf_name}, {season})")
            profile = conference_season.get_profile(conf_name, season)
            
            logger.info(f"Profile keys: {list(profile.keys())}")
            logger.info(f"Conference: {profile['conference']}")
            logger.info(f"Number of teams: {len(profile['teams'])}")
            logger.info(f"Number of games: {len(profile['games'])}")
            logger.info(f"Number of standings: {len(profile['standings'])}")
            
            # Check the format of games
            if profile['games']:
                logger.info("First game data structure:")
                first_game = profile['games'][0]
                if hasattr(first_game, '__dict__'):
                    logger.info(f"Game is an object with attributes: {dir(first_game)}")
                    logger.info(f"Game __dict__: {first_game.__dict__}")
                else:
                    logger.info(f"Game is a dictionary with keys: {list(first_game.keys())}")
        except Exception as e:
            logger.error(f"Error getting profile for {conf_name}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
    
    logger.info("ConferenceSeason test completed")

if __name__ == "__main__":
    test_conference_season() 