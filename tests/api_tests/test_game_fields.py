"""
Test script specifically for game fields with focus on conferenceGame field.
"""
import os
import sys
import logging
import pandas as pd
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

def test_game_fields():
    """Test game fields, particularly conferenceGame, to understand their structure and behavior."""
    logger.info("Starting game fields test")
    
    # Initialize the client with API key from environment
    api_key = os.getenv('CBBD_API_KEY') or os.getenv('CFBD_API_KEY')
    if not api_key:
        logger.error("No API key found in environment variables. Set CBBD_API_KEY or CFBD_API_KEY.")
        return
    
    logger.info(f"Using API key: {api_key[:5]}..." if api_key else "No API key found")
    client = CBBDClient(api_key=api_key)
    
    # Test with SEC conference in 2025
    logger.info("Testing game fields for SEC conference in 2025")
    conference = "SEC"
    season = 2025
    
    # Get conference profile using the advanced API
    logger.info(f"Getting {conference} conference profile for {season}")
    try:
        conference_season = client.advanced.conference_season
        profile = conference_season.get_profile(conference, season)
        
        # Basic validation
        logger.info(f"Profile retrieved with {len(profile.get('games', []))} games")
        
        # Create DataFrame from games for analysis
        if 'games' in profile and profile['games']:
            games_df = pd.DataFrame(profile['games'])
            logger.info(f"Created DataFrame with {len(games_df)} games")
            
            # 1. Check if conferenceGame field exists
            logger.info(f"DataFrame columns: {list(games_df.columns)}")
            has_conference_game = 'conferenceGame' in games_df.columns
            logger.info(f"Has conferenceGame field: {has_conference_game}")
            
            if has_conference_game:
                # 2. Check the data type of conferenceGame field
                logger.info(f"conferenceGame dtype: {games_df['conferenceGame'].dtype}")
                
                # 3. Check value distribution
                value_counts = games_df['conferenceGame'].value_counts().to_dict()
                logger.info(f"conferenceGame value counts: {value_counts}")
                
                # 4. Check for NaN values
                nan_count = games_df['conferenceGame'].isna().sum()
                logger.info(f"NaN values in conferenceGame: {nan_count}")
                
                # 5. Get unique values
                unique_values = games_df['conferenceGame'].unique()
                logger.info(f"Unique values in conferenceGame: {unique_values}")
                
                # 6. Check sample values
                logger.info("Sample conferenceGame values:")
                for i, game in games_df.head(5).iterrows():
                    logger.info(f"Game {i} - conferenceGame: {game['conferenceGame']} - Type: {type(game['conferenceGame'])}")
                
                # 7. Test boolean conversion
                logger.info("Testing boolean conversion:")
                try:
                    # Try direct conversion
                    games_df['conferenceGame_bool'] = games_df['conferenceGame'].astype(bool)
                    logger.info(f"Direct bool conversion result counts: {games_df['conferenceGame_bool'].value_counts().to_dict()}")
                    
                    # Try explicit True comparison
                    games_df['conferenceGame_is_true'] = games_df['conferenceGame'] == True
                    logger.info(f"Explicit == True comparison counts: {games_df['conferenceGame_is_true'].value_counts().to_dict()}")
                    
                    # Try various mappings
                    # Method 1: Map string values
                    if games_df['conferenceGame'].dtype == 'object':
                        mapping = {True: True, 'True': True, 'true': True, 
                                  False: False, 'False': False, 'false': False}
                        games_df['conferenceGame_mapped'] = games_df['conferenceGame'].map(mapping)
                        logger.info(f"String mapping conversion counts: {games_df['conferenceGame_mapped'].value_counts().to_dict()}")
                    
                    # Method 2: Try int conversion first then bool
                    try:
                        games_df['conferenceGame_int_bool'] = games_df['conferenceGame'].astype(int).astype(bool)
                        logger.info(f"Int->Bool conversion counts: {games_df['conferenceGame_int_bool'].value_counts().to_dict()}")
                    except Exception as e:
                        logger.info(f"Int->Bool conversion failed: {str(e)}")
                    
                except Exception as e:
                    logger.error(f"Error during boolean conversion: {str(e)}")
                
                # 8. Count conference games using different methods
                logger.info("Counting conference games using different methods:")
                
                # Method 1: Direct True comparison
                true_count = (games_df['conferenceGame'] == True).sum()
                logger.info(f"Count using == True: {true_count}")
                
                # Method 2: Boolean conversion
                bool_count = games_df['conferenceGame'].astype(bool).sum()
                logger.info(f"Count using .astype(bool).sum(): {bool_count}")
                
                # Method 3: Using .eq and sum
                eq_count = games_df['conferenceGame'].eq(True).sum()
                logger.info(f"Count using .eq(True).sum(): {eq_count}")
                
                # 9. Examine sample conference games
                logger.info("Sample of games where conferenceGame is True:")
                conf_games = games_df[games_df['conferenceGame'] == True]
                for i, game in conf_games.head(3).iterrows():
                    logger.info(f"Game {i}: {game['awayTeam']} @ {game['homeTeam']}")
                
                # 10. Examine the home/away conference fields
                if 'homeConference' in games_df.columns and 'awayConference' in games_df.columns:
                    logger.info("Examining home/away conference fields")
                    # Count games where both teams are from the same conference
                    same_conf_count = (games_df['homeConference'] == games_df['awayConference']).sum()
                    logger.info(f"Games with same home/away conference: {same_conf_count}")
                    
                    # Compare with conferenceGame field
                    if same_conf_count != true_count:
                        logger.warning(f"Mismatch between same conference count ({same_conf_count}) and conferenceGame true count ({true_count})")
                        
                        # Check for discrepancies
                        same_conf_mask = games_df['homeConference'] == games_df['awayConference']
                        conf_game_mask = games_df['conferenceGame'] == True
                        
                        # Games that are conference games but teams aren't from same conference
                        conf_game_but_diff_conf = games_df[conf_game_mask & ~same_conf_mask]
                        logger.info(f"Games marked as conference but teams from different conferences: {len(conf_game_but_diff_conf)}")
                        
                        # Games that aren't conference games but teams are from same conference
                        same_conf_but_not_conf_game = games_df[same_conf_mask & ~conf_game_mask]
                        logger.info(f"Games with teams from same conference but not marked as conference: {len(same_conf_but_not_conf_game)}")
            else:
                logger.warning("conferenceGame field not found in the DataFrame")
                
                # Check home/away conference fields as alternative
                if 'homeConference' in games_df.columns and 'awayConference' in games_df.columns:
                    # Count games where both teams are from the same conference
                    same_conf_count = (games_df['homeConference'] == games_df['awayConference']).sum()
                    logger.info(f"Games with same home/away conference: {same_conf_count}")
        else:
            logger.warning("No games found in the profile")
            
    except Exception as e:
        logger.error(f"Error testing game fields: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    logger.info("Game fields test completed")

if __name__ == "__main__":
    test_game_fields() 