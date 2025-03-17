"""
Streamlit app for demonstrating the CBBD Python SDK.
"""

import os
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from dotenv import load_dotenv
import numpy as np

from cbbd import CBBDClient

# Load environment variables
load_dotenv()

# Constants
DEFAULT_SEASON = 2023
DEFAULT_TEAM = "Duke"
DEFAULT_CONFERENCE = "ACC"

# Configure the page
st.set_page_config(
    page_title="CBBD Python SDK Demo",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .subsection-header {
        font-size: 1.4rem;
        font-weight: bold;
        color: #4338CA;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .info-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #3B82F6;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar - Authentication
st.sidebar.markdown("### Authentication")

api_key = st.sidebar.text_input(
    "API Key",
    value=os.getenv("CBBD_API_KEY", ""),
    type="password",
    help="Enter your CBBD API key. You can get one from collegebasketballdata.com"
)

if not api_key:
    st.sidebar.warning("Please enter your API key to use the app.")

# Initialize the client if API key is provided
client = None
if api_key:
    try:
        client = CBBDClient(api_key=api_key)
        st.sidebar.success("API key accepted!")
    except Exception as e:
        st.sidebar.error(f"Error initializing client: {e}")

# Sidebar - Navigation
st.sidebar.markdown("### Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    [
        "Home",
        "Teams",
        "Games",
        "Stats",
        "Rankings",
        "Ratings",
        "Plays",
        "Lines",
        "Transformers",
        "Advanced Analysis",
    ]
)

# Sidebar - Filters
st.sidebar.markdown("### Filters")

season = st.sidebar.selectbox(
    "Season",
    list(range(2025, 2010, -1)),
    index=0
)

# Get teams for the dropdown (if client is initialized)
teams = []
conferences = []
if client:
    try:
        teams_data = client.teams.get_teams()
        teams = sorted([team.name for team in teams_data])
        
        conferences_data = client.conferences.get_conferences()
        conferences = sorted([conf.abbreviation for conf in conferences_data])
    except Exception as e:
        st.sidebar.error(f"Error loading teams/conferences: {e}")

team = st.sidebar.selectbox(
    "Team",
    teams if teams else ["Duke", "North Carolina", "Kentucky", "Kansas", "Gonzaga"],
    index=0 if DEFAULT_TEAM in teams else 0
)

conference = st.sidebar.selectbox(
    "Conference",
    conferences if conferences else ["ACC", "SEC", "Big 12", "Big Ten", "Pac-12"],
    index=0 if DEFAULT_CONFERENCE in conferences else 0
)

# Main content
if page == "Home":
    st.markdown('<div class="main-header">CBBD Python SDK Demo</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
        This Streamlit app demonstrates the capabilities of the College Basketball Data (CBBD) Python SDK.
        Use the sidebar to navigate through different sections and explore the various API endpoints.
        
        To get started, enter your API key in the sidebar. If you don't have one, you can get it from
        [collegebasketballdata.com](https://collegebasketballdata.com).
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SDK Overview
    st.markdown('<div class="section-header">SDK Overview</div>', unsafe_allow_html=True)
    st.markdown("""
        The CBBD Python SDK provides a structured, well-documented, and easy-to-use interface for accessing college basketball data.
        It includes:
        
        - Comprehensive API coverage for college basketball data
        - Automatic request retries and error handling
        - Simple object-oriented interface with type hints
        - Advanced functionality for data analysis and visualization
        - Detailed logging for debugging
        - Proper authentication handling
        - Caching support to reduce API calls
    """)
    
    # Available APIs
    st.markdown('<div class="section-header">Available APIs</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="subsection-header">Team Information</div>', unsafe_allow_html=True)
        st.markdown("""
            - Teams API
            - Conferences API
            - Venues API
        """)
        
        st.markdown('<div class="subsection-header">Game Data</div>', unsafe_allow_html=True)
        st.markdown("""
            - Games API
            - Plays API
            - Lines API
        """)
    
    with col2:
        st.markdown('<div class="subsection-header">Statistics</div>', unsafe_allow_html=True)
        st.markdown("""
            - Stats API
            - Rankings API
            - Ratings API
        """)
        
        st.markdown('<div class="subsection-header">Player Data</div>', unsafe_allow_html=True)
        st.markdown("""
            - Lineups API
            - Draft API
            - Recruiting API
            - Substitutions API
        """)
    
    with col3:
        st.markdown('<div class="subsection-header">Advanced Analysis</div>', unsafe_allow_html=True)
        st.markdown("""
            - Team Season Profile
            - Player Season Profile
            - Game Analysis
        """)
    
    # Example code
    st.markdown('<div class="section-header">Example Code</div>', unsafe_allow_html=True)
    
    st.code("""
# Initialize client with your API key
from cbbd import CBBDClient
client = CBBDClient(api_key="your-api-key")

# Get team information
teams = client.teams.get_teams()
for team in teams:
    print(f"{team.name} ({team.conference})")

# Get games for a specific team and season
games = client.games.get_games(team="Duke", season=2023)
for game in games:
    print(f"{game.away_team} @ {game.home_team}: {game.away_points}-{game.home_points}")

# Advanced functionality
profile = client.advanced.team_season.get_profile(team="Duke", season=2023)
print(f"Team stats: {profile['stats']}")
    """, language="python")

elif page == "Teams" and client:
    st.markdown('<div class="main-header">Teams</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Teams", "Roster"])
    
    with tab1:
        try:
            with st.spinner("Loading teams data..."):
                teams_data = client.teams.get_teams(conference=conference)
                
                if teams_data:
                    # Show a sample of the raw data in expandable section
                    with st.expander("Raw Data Sample"):
                        if len(teams_data) > 0:
                            if hasattr(teams_data[0], 'get_raw_data'):
                                st.json(teams_data[0].get_raw_data())
                            else:
                                # If get_raw_data is not available, try to get the dictionary representation
                                try:
                                    st.json(teams_data[0].__dict__.get('_data', {}))
                                except:
                                    st.write("Raw data not available")
                    
                    # Convert to DataFrame for better display
                    teams_df = pd.DataFrame([
                        {
                            "Team": team.name,
                            "Mascot": team.mascot,
                            "Conference": team.conference,
                            "Abbreviation": team.abbreviation,
                            "City": team.city,
                            "State": team.state,
                            "Venue": team.venue
                        } for team in teams_data
                    ])
                    
                    st.dataframe(teams_df)
                    
                    # Display conference distribution
                    conf_counts = teams_df["Conference"].value_counts().reset_index()
                    conf_counts.columns = ["Conference", "Count"]
                    
                    chart = alt.Chart(conf_counts).mark_bar().encode(
                        x=alt.X("Conference", sort="-y"),
                        y="Count",
                        color=alt.Color("Conference", legend=None)
                    ).properties(
                        title="Teams by Conference",
                        width=600,
                        height=400
                    )
                    
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning("No teams data found.")
        except Exception as e:
            st.error(f"Error loading teams data: {e}")
    
    with tab2:
        try:
            with st.spinner(f"Loading roster data for {team} ({season})..."):
                roster = client.teams.get_roster(team=team, season=season)
                
                if roster and (hasattr(roster, 'players') and roster.players):
                    # Show a sample of the raw data in expandable section
                    with st.expander("Raw Data Sample"):
                        if len(roster.players) > 0:
                            if hasattr(roster.players[0], 'get_raw_data'):
                                st.json(roster.players[0].get_raw_data())
                            else:
                                # If get_raw_data is not available, try to get the dictionary representation
                                try:
                                    st.json(roster.players[0].__dict__.get('_data', {}))
                                except:
                                    st.write("Raw data not available")
                    
                    # First let's examine what data is actually in the first player
                    with st.expander("Debug Player Raw Data Structure"):
                        if len(roster.players) > 0:
                            player = roster.players[0]
                            st.write(f"Player dict keys: {dir(player)}")
                            if hasattr(player, '_data'):
                                st.json(player._data)
                            if hasattr(player, 'get_raw_data'):
                                st.json(player.get_raw_data())
                            
                            # DEBUG: Show the full roster raw data
                            st.subheader("Full Roster Raw Data")
                            if hasattr(roster, '_data'):
                                roster_data = roster._data
                                st.json(roster_data)
                                st.write(f"Number of players in raw data: {len(roster_data.get('players', []))}")
                    
                    # Extract data directly from the roster's raw data
                    try:
                        # First try to get the raw data from the roster object directly
                        if hasattr(roster, '_data') and roster._data and 'players' in roster._data:
                            raw_players = roster._data['players']
                        elif hasattr(roster, 'get_raw_data'):
                            raw_data = roster.get_raw_data()
                            raw_players = raw_data.get('players', [])
                        else:
                            # Fallback to the players list
                            raw_players = []
                            for player in roster.players:
                                if hasattr(player, '_data'):
                                    raw_players.append(player._data)
                                elif hasattr(player, 'get_raw_data'):
                                    raw_players.append(player.get_raw_data())
                        
                        # Debug the raw players array
                        with st.expander("Raw Players Array"):
                            st.write(f"Number of players in raw array: {len(raw_players)}")
                            if raw_players:
                                st.json(raw_players[0])  # Show first player as sample
                        
                        # Extract data directly from raw player dictionaries
                        roster_data = []
                        
                        # Check if we're dealing with the team object containing a players array
                        if len(raw_players) == 1 and isinstance(raw_players[0], dict) and 'players' in raw_players[0]:
                            # We have a team object with players array
                            team_obj = raw_players[0]
                            player_array = team_obj.get('players', [])
                            st.success(f"Extracted players array with {len(player_array)} players")
                            
                            # Iterate through each player in the array
                            for i, player_dict in enumerate(player_array):
                                player_data = {}
                                
                                # Extract basic information
                                player_data["Name"] = player_dict.get('name', '')
                                player_data["Jersey"] = player_dict.get('jersey', '')
                                player_data["Position"] = player_dict.get('position', '')
                                player_data["Height"] = player_dict.get('height', None)
                                player_data["Weight"] = player_dict.get('weight', None)
                                player_data["Year"] = player_dict.get('year', '')
                                
                                # Extract hometown information
                                hometown_dict = player_dict.get('hometown', {}) or {}
                                if hometown_dict:
                                    player_data["City"] = hometown_dict.get('city', '')
                                    player_data["State"] = hometown_dict.get('state', '')
                                    player_data["Country"] = hometown_dict.get('country', '')
                                    player_data["Latitude"] = hometown_dict.get('latitude', None)
                                    player_data["Longitude"] = hometown_dict.get('longitude', None)
                                else:
                                    # Fallback to direct attributes
                                    player_data["City"] = ''
                                    player_data["State"] = player_dict.get('home_state', '')
                                    player_data["Country"] = player_dict.get('home_country', '')
                                    player_data["Latitude"] = None
                                    player_data["Longitude"] = None
                                
                                # Extract season information
                                player_data["Start Season"] = player_dict.get('startSeason', None)
                                if player_data["Start Season"]:
                                    player_data["Experience"] = season - player_data["Start Season"]
                                else:
                                    player_data["Experience"] = 0
                                
                                roster_data.append(player_data)
                        else:
                            # Process as before - direct player objects
                            for player_dict in raw_players:
                                player_data = {}
                                
                                # Extract basic information
                                player_data["Name"] = player_dict.get('name', '')
                                player_data["Jersey"] = player_dict.get('jersey', '')
                                player_data["Position"] = player_dict.get('position', '')
                                player_data["Height"] = player_dict.get('height', None)
                                player_data["Weight"] = player_dict.get('weight', None)
                                player_data["Year"] = player_dict.get('year', '')
                                
                                # Extract hometown information
                                hometown_dict = player_dict.get('hometown', {}) or {}
                                if hometown_dict:
                                    player_data["City"] = hometown_dict.get('city', '')
                                    player_data["State"] = hometown_dict.get('state', '')
                                    player_data["Country"] = hometown_dict.get('country', '')
                                    player_data["Latitude"] = hometown_dict.get('latitude', None)
                                    player_data["Longitude"] = hometown_dict.get('longitude', None)
                                else:
                                    # Fallback to direct attributes
                                    player_data["City"] = ''
                                    player_data["State"] = player_dict.get('home_state', '')
                                    player_data["Country"] = player_dict.get('home_country', '')
                                    player_data["Latitude"] = None
                                    player_data["Longitude"] = None
                                
                                # Extract season information
                                player_data["Start Season"] = player_dict.get('startSeason', None)
                                if player_data["Start Season"]:
                                    player_data["Experience"] = season - player_data["Start Season"]
                                else:
                                    player_data["Experience"] = 0
                                
                                roster_data.append(player_data)
                    except Exception as e:
                        st.error(f"Error extracting player data: {e}")
                        import traceback
                        st.text(traceback.format_exc())
                        roster_data = []
                    
                    # Convert to DataFrame
                    roster_df = pd.DataFrame(roster_data)
                    
                    # Display raw DataFrame for debugging
                    with st.expander("Debug DataFrame"):
                        st.dataframe(roster_df)
                    
                    # Build hometown string from available data
                    def build_hometown(row):
                        city = row.get('City', '')
                        state = row.get('State', '')
                        country = row.get('Country', '')
                        
                        # Filter out NULL and empty values
                        if city and city.lower() == 'null':
                            city = ''
                        if state and state.lower() == 'null':
                            state = ''
                        if country and country.lower() == 'null':
                            country = ''
                            
                        # Build the string based on available data
                        if city and (state or country):
                            location = state if state else country
                            return f"{city}, {location}"
                        elif city:
                            return city
                        elif state:
                            return state
                        elif country:
                            return country
                        else:
                            return ""
                    
                    roster_df["Hometown"] = roster_df.apply(build_hometown, axis=1)
                    
                    # Clean up data - remove incomplete entries and fix formatting
                    # Convert numeric columns properly
                    for col in ['Height', 'Weight', 'Latitude', 'Longitude']:
                        if col in roster_df.columns:
                            # Convert string 'NULL' to NaN first
                            roster_df[col] = roster_df[col].replace('NULL', np.nan)
                            # Then convert to numeric
                            roster_df[col] = pd.to_numeric(roster_df[col], errors='coerce')
                    
                    # Replace 'NULL' string values with empty strings in text columns
                    for col in ['City', 'State', 'Country', 'Name', 'Position', 'Jersey']:
                        if col in roster_df.columns:
                            roster_df[col] = roster_df[col].replace('NULL', '')
                            # Also replace None with empty string
                            roster_df[col] = roster_df[col].fillna('')
                    
                    # Display roster in a clean table
                    st.subheader(f"{team} Roster ({season})")
                    # Sort by jersey number
                    display_df = roster_df.copy()
                    # Convert jersey to numeric for sorting, but handle non-numeric values
                    display_df["Jersey"] = pd.to_numeric(display_df["Jersey"], errors='coerce')
                    display_df = display_df.sort_values("Jersey")
                    display_cols = ["Jersey", "Name", "Position", "Height", "Weight", "Hometown", "Experience"]
                    st.dataframe(display_df[display_cols])
                    
                    # Check if we have enough data for meaningful visualizations
                    has_position_data = not roster_df["Position"].isna().all() and not (roster_df["Position"] == "").all() and len(roster_df["Position"].unique()) > 1
                    has_height_weight = not roster_df["Height"].isna().all() and not roster_df["Weight"].isna().all() and not (roster_df["Height"] == 0).all() and not (roster_df["Weight"] == 0).all()
                    has_hometown_data = not roster_df["Hometown"].isna().all() and not (roster_df["Hometown"] == "").all()
                    has_map_data = not roster_df.dropna(subset=["Latitude", "Longitude"]).empty
                    
                    # Create tabs for different visualizations
                    roster_viz_tab1, roster_viz_tab2, roster_viz_tab3 = st.tabs(["Hometown Map", "Physical Attributes", "Position Breakdown"])
                    
                    with roster_viz_tab1:
                        # Map of player hometowns
                        st.subheader("Player Hometowns")
                        
                        if has_hometown_data:
                            # Debug the hometown data
                            with st.expander("Debug Hometown Data"):
                                st.write("Players with hometown data:")
                                hometown_debug = roster_df[["Name", "City", "State", "Country", "Latitude", "Longitude", "Hometown"]]
                                st.dataframe(hometown_debug)
                            
                            # Filter out players without coordinates
                            map_df = roster_df.dropna(subset=["Latitude", "Longitude"])
                            
                            if has_map_data and not map_df.empty:
                                # Create a map centered on the US
                                map_center = {"lat": 39.8283, "lon": -98.5795}
                                
                                # Create a DataFrame for the map
                                map_data = pd.DataFrame({
                                    "lat": map_df["Latitude"],
                                    "lon": map_df["Longitude"],
                                    "player": map_df["Name"],
                                    "position": map_df["Position"],
                                    "hometown": map_df["Hometown"]
                                })
                                
                                # Ensure lat/lon are numeric
                                map_data["lat"] = pd.to_numeric(map_data["lat"], errors='coerce')
                                map_data["lon"] = pd.to_numeric(map_data["lon"], errors='coerce')
                                map_data = map_data.dropna(subset=["lat", "lon"])
                                
                                if not map_data.empty:
                                    st.map(map_data, zoom=3)
                                else:
                                    st.warning("Map data could not be properly processed. Showing text-based view instead.")
                            
                            # Always show text-based visualization as a backup/complement
                            st.subheader("Player Hometowns (Text View)")
                            hometown_data = roster_df[["Name", "Position", "Hometown"]].copy()
                            hometown_data = hometown_data[hometown_data["Hometown"] != ""]
                            if not hometown_data.empty:
                                st.dataframe(hometown_data.sort_values("Name"))
                            
                            # Show hometown breakdown by state if we have states
                            if "State" in roster_df.columns:
                                state_data = roster_df[(roster_df["State"] != "") | (roster_df["Country"] != "")]
                                
                                if not state_data.empty:
                                    # Create a location column that uses either State or Country
                                    state_data["Location"] = state_data.apply(
                                        lambda row: row["State"] if row["State"] and row["State"] != "" else row["Country"], 
                                        axis=1
                                    )
                                    
                                    # Remove any empty locations
                                    state_data = state_data[state_data["Location"] != ""]
                                    
                                    if not state_data.empty:
                                        state_counts = state_data["Location"].value_counts().reset_index()
                                        state_counts.columns = ["Location", "Count"]
                                        
                                        st.subheader("Players by State/Country")
                                        if len(state_counts) > 0:
                                            chart = alt.Chart(state_counts).mark_bar().encode(
                                                x=alt.X("Count:Q"),
                                                y=alt.Y("Location:N", sort="-x"),
                                                tooltip=["Location", "Count"]
                                            ).properties(
                                                height=min(400, len(state_counts) * 25)
                                            )
                                            st.altair_chart(chart, use_container_width=True)
                                        
                                        # List all players by state/country
                                        st.subheader("Roster by Location")
                                        for location in state_counts["Location"]:
                                            players_from_location = state_data[state_data["Location"] == location]
                                            st.markdown(f"**{location}** ({len(players_from_location)}): " + 
                                                        ", ".join(players_from_location["Name"].tolist()))
                        else:
                            st.warning("No hometown data available for this team.")
                    
                    with roster_viz_tab2:
                        st.subheader("Player Physical Attributes")
                        
                        if has_height_weight:
                            # Filter out missing height/weight values
                            phys_df = roster_df.dropna(subset=["Height", "Weight"])
                            phys_df = phys_df[(phys_df["Height"] > 0) & (phys_df["Weight"] > 0)]
                            
                            # Convert height to feet and inches for display
                            phys_df["Height_display"] = phys_df["Height"].apply(
                                lambda x: f"{int(x / 12)}'{x % 12}\"" if pd.notna(x) and x > 0 else "Unknown"
                            )
                            
                            # Show height and weight ranges
                            if not phys_df.empty:
                                height_min = phys_df["Height"].min()
                                height_max = phys_df["Height"].max()
                                weight_min = phys_df["Weight"].min()
                                weight_max = phys_df["Weight"].max()
                                
                                st.markdown(f"**Height Range:** {int(height_min/12)}'{height_min%12}\" - {int(height_max/12)}'{height_max%12}\"")
                                st.markdown(f"**Weight Range:** {weight_min} - {weight_max} lbs")
                                
                                if len(phys_df) >= 3:  # Only create scatter plot if we have enough data points
                                    scatter = alt.Chart(phys_df).mark_circle(size=100).encode(
                                        x=alt.X("Weight:Q", title="Weight (lbs)"),
                                        y=alt.Y("Height:Q", title="Height (inches)"),
                                        color=alt.Color("Position:N", scale=alt.Scale(scheme="category10")),
                                        tooltip=["Name", "Position", "Height_display", "Weight"]
                                    ).properties(
                                        title=f"Height vs Weight by Position",
                                        width=600,
                                        height=400
                                    )
                                    
                                    st.altair_chart(scatter, use_container_width=True)
                                
                                # Height distribution - only if we have multiple heights
                                if phys_df["Height"].nunique() > 1:
                                    height_chart = alt.Chart(phys_df).mark_bar().encode(
                                        x=alt.X("Height:Q", bin=alt.Bin(maxbins=10), title="Height (inches)"),
                                        y=alt.Y("count()", title="Number of Players"),
                                        color=alt.Color("Position:N", scale=alt.Scale(scheme="category10"))
                                    ).properties(
                                        title="Height Distribution",
                                        width=600,
                                        height=200
                                    )
                                    
                                    st.altair_chart(height_chart, use_container_width=True)
                                
                                # Table of players sorted by height (tallest to shortest)
                                st.subheader("Players Ranked by Height")
                                height_sorted = phys_df.sort_values("Height", ascending=False)
                                height_table = height_sorted[["Name", "Position", "Height_display", "Weight"]]
                                st.dataframe(height_table)
                            else:
                                st.warning("No valid height and weight data found after filtering.")
                        else:
                            st.warning("Height and weight data not available for this team.")
                    
                    with roster_viz_tab3:
                        st.subheader("Position Breakdown")
                        
                        if has_position_data:
                            # Position distribution
                            pos_counts = roster_df["Position"].value_counts().reset_index()
                            pos_counts.columns = ["Position", "Count"]
                            
                            if len(pos_counts) > 1:  # Only create chart if we have multiple positions
                                # Pie chart for positions
                                position_fig, ax = plt.subplots(figsize=(8, 8))
                                ax.pie(pos_counts["Count"], labels=pos_counts["Position"], autopct='%1.1f%%', 
                                      startangle=90, shadow=False)
                                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                                plt.title(f"Position Breakdown for {team} ({season})")
                                st.pyplot(position_fig)
                            
                            # Table of players by position
                            st.subheader("Players by Position")
                            for position in pos_counts["Position"]:
                                position_players = roster_df[roster_df["Position"] == position]
                                st.markdown(f"**{position}** ({len(position_players)}): " + 
                                            ", ".join(position_players["Name"].tolist()))

                            # Position breakdown
                            for position in sorted(roster_df["Position"].unique()):
                                position_players = roster_df[roster_df["Position"] == position].sort_values("Jersey")
                                st.markdown(f"**{position}** ({len(position_players)}): " + 
                                        ", ".join(position_players["Name"].tolist()))
                            
                            # Position experience breakdown - only if we have experience data
                            if "Experience" in roster_df.columns and not roster_df["Experience"].isna().all():
                                exp_by_pos = roster_df.groupby("Position")["Experience"].mean().reset_index()
                                exp_by_pos.columns = ["Position", "Avg Experience"]
                                
                                if len(exp_by_pos) > 1:  # Only create chart if we have multiple positions
                                    exp_chart = alt.Chart(exp_by_pos).mark_bar().encode(
                                        x=alt.X("Position:N"),
                                        y=alt.Y("Avg Experience:Q"),
                                        color=alt.Color("Position:N", scale=alt.Scale(scheme="category10")),
                                        tooltip=["Position", "Avg Experience"]
                                    ).properties(
                                        title="Average Experience by Position (Years)",
                                        width=600,
                                        height=300
                                    )
                                    
                                    st.altair_chart(exp_chart, use_container_width=True)
                            else:
                                st.warning("Position data not available or uniform for this team.")
                        else:
                            st.warning(f"No roster data found for {team} in {season}.")
        except Exception as e:
            st.error(f"Error loading roster data: {e}")
            import traceback
            st.text(traceback.format_exc())

elif page == "Games" and client:
    st.markdown('<div class="main-header">Games</div>', unsafe_allow_html=True)
    
    try:
        with st.spinner(f"Loading games data for {team} ({season})..."):
            games_data = client.games.get_games(team=team, season=season)
            
            if games_data:
                # Show a sample of the raw data in expandable section
                with st.expander("Raw Data Sample"):
                    if len(games_data) > 0:
                        if hasattr(games_data[0], 'get_raw_data'):
                            st.json(games_data[0].get_raw_data())
                        else:
                            # If get_raw_data is not available, try to get the dictionary representation
                            try:
                                st.json(games_data[0].__dict__.get('_data', {}))
                            except:
                                st.write("Raw data not available")
                
                # Convert to DataFrame for better display
                games_df = pd.DataFrame([
                    {
                        "Date": game.start_date,
                        "Home Team": game.home_team,
                        "Away Team": game.away_team,
                        "Home Score": game.home_points,
                        "Away Score": game.away_points,
                        "Status": game.status,
                        "Home Winner": game.home_winner,
                        "Away Winner": game.away_winner,
                        "Venue": game.venue,
                        "Conference Game": game.conference_game,
                        "Neutral Site": game.neutral_site
                    } for game in games_data
                ])
                
                st.dataframe(games_df)
                
                # Calculate and display wins and losses
                wins = len(games_df[(games_df["Home Team"] == team) & (games_df["Home Winner"] == True)]) + \
                       len(games_df[(games_df["Away Team"] == team) & (games_df["Away Winner"] == True)])
                
                losses = len(games_df[(games_df["Home Team"] == team) & (games_df["Home Winner"] == False)]) + \
                         len(games_df[(games_df["Away Team"] == team) & (games_df["Away Winner"] == False)])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Wins", wins)
                
                with col2:
                    st.metric("Losses", losses)
                
                # Plot points over time
                team_points = []
                opponent_points = []
                dates = []
                
                for _, game in games_df.iterrows():
                    date = game["Date"]
                    
                    if game["Home Team"] == team:
                        team_points.append(game["Home Score"])
                        opponent_points.append(game["Away Score"])
                    else:
                        team_points.append(game["Away Score"])
                        opponent_points.append(game["Home Score"])
                    
                    dates.append(date)
                
                scoring_df = pd.DataFrame({
                    "Date": dates,
                    "Team Points": team_points,
                    "Opponent Points": opponent_points
                })
                
                chart = alt.Chart(scoring_df).transform_fold(
                    ["Team Points", "Opponent Points"],
                    as_=["Metric", "Points"]
                ).mark_line(point=True).encode(
                    x="Date:T",
                    y="Points:Q",
                    color="Metric:N",
                    tooltip=["Date:T", "Points:Q", "Metric:N"]
                ).properties(
                    title=f"Points per Game for {team} ({season})",
                    width=700,
                    height=400
                )
                
                st.altair_chart(chart, use_container_width=True)
            else:
                st.warning(f"No games data found for {team} in {season}.")
    except Exception as e:
        st.error(f"Error loading games data: {e}")

elif page == "Stats" and client:
    st.markdown('<div class="main-header">Statistics</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Team Stats", "Player Stats"])
    
    with tab1:
        try:
            with st.spinner(f"Loading team stats for {team} ({season})..."):
                team_stats = client.stats.get_team_stats(team=team, season=season)
                
                if team_stats:
                    # Show a sample of the raw data in expandable section
                    with st.expander("Raw Data Sample"):
                        if len(team_stats) > 0:
                            if hasattr(team_stats[0], 'get_raw_data'):
                                st.json(team_stats[0].get_raw_data())
                            else:
                                # If get_raw_data is not available, try to get the dictionary representation
                                try:
                                    st.json(team_stats[0].__dict__.get('_data', {}))
                                except:
                                    st.write("Raw data not available")
                    
                    # Convert to a dictionary for easier display
                    stats_dict = {}
                    
                    for stat in team_stats:
                        for key, value in stat.to_dict().items():
                            if isinstance(value, dict):
                                for subkey, subvalue in value.items():
                                    stats_dict[f"{key}_{subkey}"] = subvalue
                            else:
                                stats_dict[key] = value
                    
                    # Display team stats in columns
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown('<div class="subsection-header">General</div>', unsafe_allow_html=True)
                        st.metric("Games", stats_dict.get("games", 0))
                        st.metric("Wins", stats_dict.get("wins", 0))
                        st.metric("Losses", stats_dict.get("losses", 0))
                        st.metric("Points per Game", round(stats_dict.get("points_total", 0) / stats_dict.get("games", 1), 1))
                    
                    with col2:
                        st.markdown('<div class="subsection-header">Shooting</div>', unsafe_allow_html=True)
                        st.metric("FG%", f"{stats_dict.get('field_goals_pct', 0):.1%}")
                        st.metric("3PT%", f"{stats_dict.get('three_point_field_goals_pct', 0):.1%}")
                        st.metric("FT%", f"{stats_dict.get('free_throws_pct', 0):.1%}")
                        st.metric("eFG%", f"{stats_dict.get('effective_field_goal_pct', 0):.1%}")
                    
                    with col3:
                        st.markdown('<div class="subsection-header">Other</div>', unsafe_allow_html=True)
                        st.metric("Rebounds", stats_dict.get("rebounds_total", 0))
                        st.metric("Assists", stats_dict.get("assists", 0))
                        st.metric("Steals", stats_dict.get("steals", 0))
                        st.metric("Blocks", stats_dict.get("blocks", 0))
                else:
                    st.warning(f"No team stats found for {team} in {season}.")
        except Exception as e:
            st.error(f"Error loading team stats: {e}")
    
    with tab2:
        try:
            with st.spinner(f"Loading player stats for {team} ({season})..."):
                player_stats = client.stats.get_player_stats(team=team, season=season)
                
                if player_stats:
                    # Show a sample of the raw data in expandable section
                    with st.expander("Raw Data Sample"):
                        if len(player_stats) > 0:
                            if hasattr(player_stats[0], 'get_raw_data'):
                                st.json(player_stats[0].get_raw_data())
                            else:
                                # If get_raw_data is not available, try to get the dictionary representation
                                try:
                                    st.json(player_stats[0].__dict__.get('_data', {}))
                                except:
                                    st.write("Raw data not available")
                    
                    # Convert to DataFrame for better display
                    player_df = pd.DataFrame([
                        {
                            "Name": stat.name,
                            "Position": stat.position,
                            "Games": stat.games,
                            "Minutes": stat.minutes,
                            "Points": stat.points,
                            "Rebounds": stat.rebounds.total if hasattr(stat.rebounds, 'total') else 0,
                            "Assists": stat.assists,
                            "Steals": stat.steals,
                            "Blocks": stat.blocks,
                            "FG%": stat.field_goals.pct if hasattr(stat.field_goals, 'pct') else 0,
                            "3PT%": stat.three_point_field_goals.pct if hasattr(stat.three_point_field_goals, 'pct') else 0,
                            "FT%": stat.free_throws.pct if hasattr(stat.free_throws, 'pct') else 0,
                        } for stat in player_stats
                    ])
                    
                    st.dataframe(player_df)
                    
                    # Top scorers visualization
                    top_scorers = player_df.nlargest(5, "Points")
                    
                    chart = alt.Chart(top_scorers).mark_bar().encode(
                        x=alt.X("Points:Q"),
                        y=alt.Y("Name:N", sort="-x"),
                        color=alt.Color("Points:Q", scale=alt.Scale(scheme="reds")),
                        tooltip=["Name", "Position", "Points", "Games"]
                    ).properties(
                        title=f"Top Scorers for {team} ({season})",
                        width=600,
                        height=300
                    )
                    
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning(f"No player stats found for {team} in {season}.")
        except Exception as e:
            st.error(f"Error loading player stats: {e}")

elif page == "Transformers" and client:
    st.markdown('<div class="main-header">Data Transformers</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
        This page demonstrates the data transformation capabilities of the CBBD SDK.
        The transformers convert API responses into pandas DataFrames for easier data analysis and visualization.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create tabs for different transformer showcases
    transformer_tabs = st.tabs([
        "Overview", 
        "Teams & Roster", 
        "Games", 
        "Players", 
        "Rankings", 
        "Lines",
        "Advanced Utilities"
    ])
    
    # Overview tab
    with transformer_tabs[0]:
        st.markdown('<div class="section-header">Transformers Overview</div>', unsafe_allow_html=True)
        
        st.markdown("""
            The CBBD SDK includes a comprehensive data transformation layer that makes working with API data much easier.
            Key features include:
            
            - Converting complex nested API responses to pandas DataFrames
            - Handling NULL values and missing data
            - Extracting nested attributes
            - Standardizing column names
            - Calculating derived values
            - Preparing data for visualization
        """)
        
        # Example usage
        st.markdown('<div class="subsection-header">Example Usage</div>', unsafe_allow_html=True)
        
        st.code("""
# Initialize the client
from cbbd import CBBDClient
client = CBBDClient(api_key="your-api-key")

# Get team roster data from the API
roster = client.teams.get_roster(team="Duke", season=2023)

# Transform to DataFrame (Option 1 - using client.transformers interface)
roster_df = client.transformers.roster_to_dataframe(roster)

# Transform to DataFrame (Option 2 - using transformer directly)
from cbbd.transformers import RosterTransformer
roster_df = RosterTransformer.to_dataframe(roster)

# Now you can use standard pandas operations
tall_players = roster_df[roster_df['height'] > 80]
avg_by_position = roster_df.groupby('position')['weight'].mean()
        """, language="python")
        
        # Available transformers table
        st.markdown('<div class="subsection-header">Available Transformers</div>', unsafe_allow_html=True)
        
        transformers_df = pd.DataFrame({
            "Transformer": [
                "RosterTransformer", 
                "TeamsTransformer", 
                "GamesTransformer", 
                "GameStatsTransformer",
                "PlayersTransformer", 
                "PlayerStatsTransformer",
                "RankingsTransformer",
                "RatingsTransformer",
                "LinesTransformer",
                "PlaysTransformer"
            ],
            "Description": [
                "Converts team roster data to DataFrame with player details",
                "Converts team information to DataFrame",
                "Converts game schedule/results to DataFrame",
                "Converts game box score statistics to DataFrame",
                "Converts player information to DataFrame",
                "Converts player statistics to DataFrame",
                "Converts rankings data to DataFrame",
                "Converts team ratings data to DataFrame",
                "Converts betting lines data to DataFrame",
                "Converts play-by-play data to DataFrame"
            ],
            "Client Method": [
                "client.transformers.roster_to_dataframe()",
                "client.transformers.teams_to_dataframe()",
                "client.transformers.games_to_dataframe()",
                "client.transformers.game_stats_to_dataframe()",
                "None (use directly)",
                "client.transformers.player_stats_to_dataframe()",
                "client.transformers.rankings_to_dataframe()",
                "client.transformers.ratings_to_dataframe()",
                "client.transformers.lines_to_dataframe()",
                "client.transformers.plays_to_dataframe()"
            ]
        })
        
        st.dataframe(transformers_df, use_container_width=True)
        
        # Utility functions
        st.markdown('<div class="subsection-header">DataFrame Utilities</div>', unsafe_allow_html=True)
        
        st.markdown("""
            The SDK also provides utility functions for working with the transformed DataFrames:
            
            - `make_visualization_ready()`: Prepare a DataFrame for visualization by ensuring proper data types
            - `add_calculated_columns()`: Add calculated columns to a DataFrame
            - `filter_season()`: Filter a DataFrame to a specific season
            - `filter_team()`: Filter a DataFrame to a specific team
            - `standardize_column_names()`: Standardize column names to snake_case format
        """)
        
        st.code("""
# Access utilities through the client
utilities = client.transformers.utils

# Make DataFrame ready for visualization
viz_df = utilities.make_visualization_ready(
    df, 
    numeric_columns=['points', 'rebounds', 'assists'],
    categorical_columns=['position', 'team'],
    date_columns=['game_date']
)

# Add calculated columns
df_with_calcs = utilities.add_calculated_columns(
    df,
    {
        'points_per_game': lambda df: df['points'] / df['games'],
        'efficiency': lambda df: (df['points'] + df['rebounds'] + df['assists']) / df['minutes']
    }
)
        """, language="python")
    
    # Teams & Roster tab
    with transformer_tabs[1]:
        st.markdown('<div class="section-header">Teams & Roster Transformers</div>', unsafe_allow_html=True)
        
        st.markdown("""
            The Teams and Roster transformers convert team information and roster data to DataFrames.
            This tab demonstrates how to use these transformers and the resulting data structure.
        """)
        
        # Get data for demonstration
        team_choice = st.selectbox("Select Team", options=teams if teams else ["Duke", "North Carolina", "Kentucky"])
        season_choice = st.selectbox("Select Season", options=list(range(2024, 2010, -1)), index=0)
        
        try:
            with st.spinner("Loading data..."):
                # Get team roster
                roster_data = client.teams.get_roster(team=team_choice, season=season_choice)
                
                # Display raw data
                if roster_data:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown('<div class="subsection-header">Raw API Response</div>', unsafe_allow_html=True)
                        with st.expander("View Raw Data", expanded=True):
                            if hasattr(roster_data, 'get_raw_data'):
                                raw_data = roster_data.get_raw_data()
                                st.json(raw_data)
                            else:
                                st.json(roster_data)
                    
                    with col2:
                        st.markdown('<div class="subsection-header">Transformed DataFrame</div>', unsafe_allow_html=True)
                        
                        # Transform to DataFrame
                        roster_df = client.transformers.roster_to_dataframe(roster_data)
                        
                        st.dataframe(roster_df, use_container_width=True)
                        
                        # Show some stats about the data
                        if not roster_df.empty:
                            st.write(f"Total players: {len(roster_df)}")
                            
                            # Show some aggregations
                            if 'position' in roster_df.columns and 'height' in roster_df.columns:
                                position_stats = roster_df.groupby('position').agg({
                                    'height': ['mean', 'std', 'count'],
                                    'weight': ['mean', 'std']
                                }).reset_index()
                                
                                st.markdown("#### Position Statistics")
                                st.dataframe(position_stats, use_container_width=True)
                
                # Example code for this transformer
                st.markdown('<div class="subsection-header">Example Code</div>', unsafe_allow_html=True)
                
                st.code(f"""
# Get roster data
roster_data = client.teams.get_roster(team="{team_choice}", season={season_choice})

# Transform to DataFrame
roster_df = client.transformers.roster_to_dataframe(roster_data)

# Now you can analyze the data with pandas
if not roster_df.empty:
    # Calculate average height by position
    avg_height = roster_df.groupby('position')['height'].mean().sort_values(ascending=False)
    print(avg_height)
    
    # Find tallest player
    tallest = roster_df.loc[roster_df['height'].idxmax()]
    print(f"Tallest player: {{tallest['name']}} ({{tallest['height']}} inches)")
    
    # Calculate experience (current season - start season)
    if 'startSeason' in roster_df.columns:
        roster_df['experience'] = {season_choice} - roster_df['startSeason']
        print(roster_df[['name', 'position', 'experience']].sort_values('experience', ascending=False))
""", language="python")
        
        except Exception as e:
            st.error(f"Error loading and transforming data: {e}")
            st.text(f"Exception details: {str(e)}")
            
    # Games tab
    with transformer_tabs[2]:
        st.markdown('<div class="section-header">Games Transformer</div>', unsafe_allow_html=True)
        
        st.markdown("""
            The Games transformer converts game schedule and results data to a DataFrame.
            This tab demonstrates how to use this transformer and the resulting data structure.
        """)
        
        # Options for demonstration
        col1, col2 = st.columns(2)
        with col1:
            demo_team = st.selectbox("Select Team", options=teams if teams else ["Duke", "North Carolina", "Kentucky"], key="games_team")
        with col2:
            demo_season = st.selectbox("Select Season", options=list(range(2024, 2010, -1)), index=0, key="games_season")
        
        try:
            with st.spinner("Loading games data..."):
                # Get games data
                games_data = client.games.get_games(team=demo_team, season=demo_season)
                
                if games_data:
                    # Raw data vs transformed data
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown('<div class="subsection-header">Raw API Response (first game)</div>', unsafe_allow_html=True)
                        with st.expander("View Raw Data", expanded=True):
                            if hasattr(games_data[0], 'get_raw_data'):
                                st.json(games_data[0].get_raw_data())
                            else:
                                st.json(games_data[0])
                    
                    with col2:
                        st.markdown('<div class="subsection-header">Transformed DataFrame</div>', unsafe_allow_html=True)
                        
                        # Transform to DataFrame
                        games_df = client.transformers.games_to_dataframe(games_data)
                        
                        # Display the DataFrame
                        st.dataframe(games_df, use_container_width=True)
                
                # Visualizations with transformed data
                if games_data and not games_df.empty:
                    st.markdown('<div class="subsection-header">Data Analysis with Transformed DataFrame</div>', unsafe_allow_html=True)
                    
                    # Show some stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Games", len(games_df))
                    
                    with col2:
                        home_games = games_df[games_df['home_team'] == demo_team]
                        st.metric("Home Games", len(home_games))
                        
                    with col3:
                        away_games = games_df[games_df['away_team'] == demo_team]
                        st.metric("Away Games", len(away_games))
                    
                    # Check if we have points data for completed games
                    if 'home_points' in games_df.columns and not games_df['home_points'].isna().all():
                        st.markdown("#### Scoring Analysis")
                        
                        # Filter to completed games
                        completed_games = games_df.dropna(subset=['home_points', 'away_points'])
                        
                        if len(completed_games) > 0:
                            # Create points scored/allowed by game
                            team_games = pd.DataFrame()
                            
                            # When team is home
                            home_df = completed_games[completed_games['home_team'] == demo_team].copy()
                            if len(home_df) > 0:
                                home_df['opponent'] = home_df['away_team']
                                home_df['points_for'] = home_df['home_points']
                                home_df['points_against'] = home_df['away_points']
                                home_df['location'] = 'Home'
                                home_df['result'] = np.where(home_df['home_points'] > home_df['away_points'], 'W', 'L')
                                team_games = pd.concat([team_games, home_df[['start_date', 'opponent', 'points_for', 'points_against', 'location', 'result']]])
                            
                            # When team is away
                            away_df = completed_games[completed_games['away_team'] == demo_team].copy()
                            if len(away_df) > 0:
                                away_df['opponent'] = away_df['home_team']
                                away_df['points_for'] = away_df['away_points']
                                away_df['points_against'] = away_df['home_points']
                                away_df['location'] = 'Away'
                                away_df['result'] = np.where(away_df['away_points'] > away_df['home_points'], 'W', 'L')
                                team_games = pd.concat([team_games, away_df[['start_date', 'opponent', 'points_for', 'points_against', 'location', 'result']]])
                            
                            # Sort by date
                            if 'start_date' in team_games.columns:
                                team_games = team_games.sort_values('start_date')
                            
                            # Display the processed data
                            st.dataframe(team_games, use_container_width=True)
                            
                            # Create a visualization
                            if len(team_games) >= 5:
                                st.markdown("#### Scoring Trend")
                                
                                # Calculate rolling averages
                                window = min(5, len(team_games))
                                team_games['points_for_avg'] = team_games['points_for'].rolling(window=window, min_periods=1).mean()
                                team_games['points_against_avg'] = team_games['points_against'].rolling(window=window, min_periods=1).mean()
                                
                                # Prepare data for chart
                                chart_data = pd.melt(
                                    team_games.reset_index(),
                                    id_vars=['start_date', 'opponent', 'result'],
                                    value_vars=['points_for', 'points_against', 'points_for_avg', 'points_against_avg'],
                                    var_name='metric',
                                    value_name='points'
                                )
                                
                                # Create line chart
                                points_chart = alt.Chart(chart_data).mark_line().encode(
                                    x=alt.X('start_date:T', title='Game Date'),
                                    y=alt.Y('points:Q', title='Points'),
                                    color=alt.Color('metric:N', title='Metric'),
                                    strokeDash=alt.condition(
                                        alt.datum.metric.contains('avg'),
                                        alt.value([5, 5]),
                                        alt.value([0])
                                    )
                                ).properties(
                                    width=700,
                                    height=400,
                                    title=f"{demo_team} Scoring Trend ({demo_season})"
                                )
                                
                                st.altair_chart(points_chart, use_container_width=True)
                                
                                # Home vs Away comparison
                                st.markdown("#### Home vs Away Performance")
                                
                                location_stats = team_games.groupby('location').agg({
                                    'points_for': 'mean',
                                    'points_against': 'mean',
                                    'result': lambda x: (x == 'W').mean() * 100  # Win percentage
                                }).reset_index()
                                
                                location_stats.columns = ['Location', 'Avg Points For', 'Avg Points Against', 'Win Percentage']
                                
                                # Display stats
                                st.dataframe(location_stats, use_container_width=True)
                
                # Example code for this transformer
                st.markdown('<div class="subsection-header">Example Code</div>', unsafe_allow_html=True)
                
                st.code(f"""
# Get games data
games_data = client.games.get_games(team="{demo_team}", season={demo_season})

# Transform to DataFrame
games_df = client.transformers.games_to_dataframe(games_data)

# Show number of games by conference
if not games_df.empty and 'away_conference' in games_df.columns:
    conf_counts = pd.concat([
        games_df[games_df['home_team'] == '{demo_team}']['away_conference'].value_counts(),
        games_df[games_df['away_team'] == '{demo_team}']['home_conference'].value_counts()
    ], axis=0).reset_index()
    conf_counts.columns = ['Conference', 'Games']
    conf_counts = conf_counts.groupby('Conference').sum().reset_index()
    print(conf_counts.sort_values('Games', ascending=False))

# Calculate scoring margin for each game
if 'home_points' in games_df.columns:
    completed_games = games_df.dropna(subset=['home_points', 'away_points'])
    
    # When team is home
    home_games = completed_games[completed_games['home_team'] == '{demo_team}'].copy()
    home_games['margin'] = home_games['home_points'] - home_games['away_points']
    
    # When team is away
    away_games = completed_games[completed_games['away_team'] == '{demo_team}'].copy()
    away_games['margin'] = away_games['away_points'] - away_games['home_points']
    
    # Combine and get average margin
    all_margins = pd.concat([home_games['margin'], away_games['margin']])
    print(f"Average margin: {{all_margins.mean():.1f}} points")
""", language="python")
                
        except Exception as e:
            st.error(f"Error loading and transforming games data: {e}")
            st.text(f"Exception details: {str(e)}")
            
    # Additional tabs will be implemented later
    
    # Players tab
    with transformer_tabs[3]:
        st.markdown('<div class="section-header">Player Stats Transformer</div>', unsafe_allow_html=True)
        
        st.markdown("""
            The Player Stats transformer converts player statistics data to a DataFrame.
            This tab demonstrates how to use this transformer and the resulting data structure.
        """)
        
        # Options for demonstration
        col1, col2 = st.columns(2)
        with col1:
            player_team = st.selectbox("Select Team", options=teams if teams else ["Duke", "North Carolina", "Kentucky"], key="players_team")
        with col2:
            player_season = st.selectbox("Select Season", options=list(range(2024, 2010, -1)), index=0, key="players_season")
        
        try:
            with st.spinner("Loading player stats..."):
                # Get player stats
                player_stats = client.stats.get_player_stats(team=player_team, season=player_season)
                
                if player_stats:
                    # Raw data vs transformed data
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown('<div class="subsection-header">Raw API Response (first player)</div>', unsafe_allow_html=True)
                        with st.expander("View Raw Data", expanded=True):
                            if hasattr(player_stats[0], 'get_raw_data'):
                                st.json(player_stats[0].get_raw_data())
                            else:
                                st.json(player_stats[0])
                    
                    with col2:
                        st.markdown('<div class="subsection-header">Transformed DataFrame</div>', unsafe_allow_html=True)
                        
                        # Transform to DataFrame
                        players_df = client.transformers.player_stats_to_dataframe(player_stats)
                        
                        # Display the DataFrame
                        st.dataframe(players_df, use_container_width=True)
                
                # Data Analysis
                if player_stats and not players_df.empty:
                    st.markdown('<div class="subsection-header">Data Analysis with Transformed DataFrame</div>', unsafe_allow_html=True)
                    
                    # Create derived metrics
                    if all(col in players_df.columns for col in ['games', 'points', 'rebounds', 'assists']):
                        # Add per-game calculations
                        players_df['ppg'] = players_df['points'] / players_df['games']
                        players_df['rpg'] = players_df['rebounds'] / players_df['games']
                        players_df['apg'] = players_df['assists'] / players_df['games']
                        
                        # Sort by points per game
                        sorted_players = players_df.sort_values('ppg', ascending=False)
                        
                        # Display players with their per-game stats
                        st.markdown("#### Player Per-Game Statistics")
                        
                        # Format the display columns
                        display_df = sorted_players[['name', 'position', 'games', 'ppg', 'rpg', 'apg']].copy()
                        for col in ['ppg', 'rpg', 'apg']:
                            display_df[col] = display_df[col].round(1)
                        
                        st.dataframe(display_df, use_container_width=True)
                        
                        # Create a visualization
                        st.markdown("#### Top Scorers")
                        
                        # Get top 10 scorers
                        top_scorers = sorted_players.head(10).copy()
                        
                        # Create bar chart
                        scorers_chart = alt.Chart(top_scorers).mark_bar().encode(
                            x=alt.X('ppg:Q', title='Points Per Game'),
                            y=alt.Y('name:N', title='Player', sort='-x'),
                            color=alt.Color('position:N', title='Position'),
                            tooltip=['name', 'position', 'ppg', 'rpg', 'apg']
                        ).properties(
                            width=600,
                            height=400,
                            title=f"Top Scorers for {player_team} ({player_season})"
                        )
                        
                        st.altair_chart(scorers_chart, use_container_width=True)
                        
                        # Position breakdown
                        if 'position' in players_df.columns:
                            st.markdown("#### Position Analysis")
                            
                            position_stats = players_df.groupby('position').agg({
                                'points': 'sum',
                                'rebounds': 'sum',
                                'assists': 'sum',
                                'games': 'mean',
                                'name': 'count'
                            }).reset_index()
                            
                            position_stats.columns = ['Position', 'Total Points', 'Total Rebounds', 'Total Assists', 'Avg Games', 'Players']
                            
                            st.dataframe(position_stats, use_container_width=True)
                            
                            # Create pie chart of scoring by position
                            if len(position_stats) > 1:
                                scoring_data = position_stats[['Position', 'Total Points']].copy()
                                scoring_data['Percentage'] = scoring_data['Total Points'] / scoring_data['Total Points'].sum() * 100
                                
                                # Create the chart
                                pie_chart = alt.Chart(scoring_data).mark_arc().encode(
                                    theta=alt.Theta(field="Total Points", type="quantitative"),
                                    color=alt.Color(field="Position", type="nominal"),
                                    tooltip=['Position', 'Total Points', 'Percentage']
                                ).properties(
                                    width=400,
                                    height=400,
                                    title=f"Scoring Distribution by Position ({player_season})"
                                )
                                
                                st.altair_chart(pie_chart, use_container_width=True)
                
                # Example code for this transformer
                st.markdown('<div class="subsection-header">Example Code</div>', unsafe_allow_html=True)
                
                st.code(f"""
# Get player stats data
player_stats = client.stats.get_player_stats(team="{player_team}", season={player_season})

# Transform to DataFrame
players_df = client.transformers.player_stats_to_dataframe(player_stats)

# Add calculated columns for per-game stats
if not players_df.empty and 'games' in players_df.columns:
    # Access DataFrame utilities
    utils = client.transformers.utils
    
    # Add calculated columns
    calculations = {{
        'ppg': lambda df: df['points'] / df['games'],
        'rpg': lambda df: df['rebounds'] / df['games'],
        'apg': lambda df: df['assists'] / df['games'],
        'efficiency': lambda df: (df['points'] + df['rebounds'] + df['assists'] - df['turnovers']) / df['minutes']
    }}
    
    players_df = utils.add_calculated_columns(players_df, calculations)
    
    # Sort by points per game and show top players
    top_players = players_df.sort_values('ppg', ascending=False).head(5)
    print(top_players[['name', 'position', 'ppg', 'rpg', 'apg', 'efficiency']])
    
    # Find the team's best 3-point shooter (min 10 attempts)
    if 'threePointFieldGoals' in players_df.columns:
        shooters = players_df[players_df['threePointFieldGoals.attempted'] >= 10].copy()
        if not shooters.empty:
            best_shooter = shooters.loc[shooters['threePointFieldGoals.pct'].idxmax()]
            print(f"Best 3PT shooter: {{best_shooter['name']}} "
                  f"({{best_shooter['threePointFieldGoals.pct']*100:.1f}}%, "
                  f"{{best_shooter['threePointFieldGoals.made']}}/{{best_shooter['threePointFieldGoals.attempted']}})")
""", language="python")
        
        except Exception as e:
            st.error(f"Error loading and transforming player stats: {e}")
            st.text(f"Exception details: {str(e)}")
    
    # Rankings tab
    with transformer_tabs[4]:
        st.markdown('<div class="section-header">Rankings Transformer</div>', unsafe_allow_html=True)
        
        st.markdown("""
            The Rankings transformer converts poll rankings data to a DataFrame.
            This tab demonstrates how to use this transformer and the resulting data structure.
        """)
        
        # Options for demonstration
        ranking_season = st.selectbox("Select Season", options=list(range(2024, 2010, -1)), index=0, key="rankings_season")
        
        try:
            with st.spinner("Loading rankings data..."):
                # Get rankings data
                rankings_data = client.rankings.get_rankings(season=ranking_season)
                
                if rankings_data:
                    # Raw data vs transformed data
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown('<div class="subsection-header">Raw API Response (sample)</div>', unsafe_allow_html=True)
                        with st.expander("View Raw Data", expanded=True):
                            if hasattr(rankings_data[0], 'get_raw_data'):
                                st.json(rankings_data[0].get_raw_data())
                            else:
                                st.json(rankings_data[0])
                    
                    with col2:
                        st.markdown('<div class="subsection-header">Transformed DataFrame</div>', unsafe_allow_html=True)
                        
                        # Transform to DataFrame
                        rankings_df = client.transformers.rankings_to_dataframe(rankings_data)
                        
                        # Display a sample of the DataFrame
                        st.dataframe(rankings_df.head(20), use_container_width=True)
                
                # Data Analysis
                if rankings_data and not rankings_df.empty:
                    st.markdown('<div class="subsection-header">Data Analysis with Transformed DataFrame</div>', unsafe_allow_html=True)
                    
                    # Poll types
                    poll_types = rankings_df['poll'].unique()
                    
                    # Create a poll selector
                    selected_poll = st.selectbox("Select Poll", options=poll_types, index=0, key="rankings_poll")
                    
                    # Filter to the selected poll
                    poll_rankings = rankings_df[rankings_df['poll'] == selected_poll]
                    
                    # Get available weeks
                    weeks = sorted(poll_rankings['week'].unique())
                    
                    if weeks:
                        # Create a week selector
                        selected_week = st.selectbox("Select Week", options=weeks, index=len(weeks)-1, key="rankings_week")
                        
                        # Filter to the selected week
                        week_rankings = poll_rankings[poll_rankings['week'] == selected_week]
                        
                        # Sort by ranking
                        sorted_rankings = week_rankings.sort_values('ranking')
                        
                        # Display the rankings for this week
                        st.markdown(f"#### {selected_poll} Rankings - Week {selected_week}")
                        
                        # Create a clean display DataFrame
                        display_cols = ['ranking', 'team', 'conference', 'points', 'first_place_votes']
                        display_cols = [col for col in display_cols if col in sorted_rankings.columns]
                        
                        st.dataframe(sorted_rankings[display_cols], use_container_width=True)
                        
                        # Create a visualization of the rankings
                        st.markdown("#### Top 25 Visualization")
                        
                        # Limit to top 25
                        top25 = sorted_rankings[sorted_rankings['ranking'] <= 25].copy()
                        
                        if not top25.empty:
                            # Conference colors
                            conf_colors = {
                                'ACC': '#007ACC',
                                'Big 12': '#FF6B00',
                                'Big East': '#0000CC',
                                'Big Ten': '#CC0000',
                                'Pac-12': '#003300',
                                'SEC': '#6600CC',
                                'American': '#006600',
                                'Atlantic 10': '#CC6600',
                                'Mountain West': '#666666'
                            }
                            
                            # Use conferences for color
                            if 'conference' in top25.columns:
                                # Create a new column for colors
                                top25['conf_color'] = top25['conference'].map(conf_colors).fillna('#999999')
                                
                                # Create horizontal bar chart
                                rankings_chart = alt.Chart(top25).mark_bar().encode(
                                    x=alt.X('points:Q', title='Points'),
                                    y=alt.Y('ranking:O', title='Rank', sort='ascending'),
                                    color=alt.Color('conference:N', title='Conference'),
                                    tooltip=['ranking', 'team', 'conference', 'points', 'first_place_votes']
                                ).properties(
                                    width=700,
                                    height=600,
                                    title=f"{selected_poll} Top 25 - Week {selected_week} ({ranking_season})"
                                )
                                
                                st.altair_chart(rankings_chart, use_container_width=True)
                                
                                # Conference breakdown
                                st.markdown("#### Conference Representation")
                                
                                conf_counts = top25['conference'].value_counts().reset_index()
                                conf_counts.columns = ['Conference', 'Teams in Top 25']
                                
                                # Display counts
                                st.dataframe(conf_counts, use_container_width=True)
                                
                                # Create pie chart
                                pie = alt.Chart(conf_counts).mark_arc().encode(
                                    theta=alt.Theta(field="Teams in Top 25", type="quantitative"),
                                    color=alt.Color(field="Conference", type="nominal"),
                                    tooltip=['Conference', 'Teams in Top 25']
                                ).properties(
                                    width=400,
                                    height=400,
                                    title=f"Conference Distribution in {selected_poll} Top 25"
                                )
                                
                                st.altair_chart(pie, use_container_width=True)
                
                # Example code for this transformer
                st.markdown('<div class="subsection-header">Example Code</div>', unsafe_allow_html=True)
                
                st.code(f"""
# Get rankings data
rankings_data = client.rankings.get_rankings(season={ranking_season})

# Transform to DataFrame
rankings_df = client.transformers.rankings_to_dataframe(rankings_data)

# Filter to AP Poll
ap_rankings = rankings_df[rankings_df['poll'] == 'AP Top 25']

# Get the final poll of the season
final_week = ap_rankings['week'].max()
final_poll = ap_rankings[ap_rankings['week'] == final_week].sort_values('ranking')

# Show top 10
print("Final AP Top 10:")
print(final_poll[['ranking', 'team', 'conference', 'points']].head(10))

# Track a specific team's ranking throughout the season
if not ap_rankings.empty:
    team_rankings = ap_rankings[ap_rankings['team'] == '{player_team}'].sort_values('week')
    
    if not team_rankings.empty:
        print(f"{{player_team}}'s AP ranking throughout the {ranking_season} season:")
        for _, row in team_rankings.iterrows():
            print(f"Week {{row['week']}}: #{row['ranking']} ({{row['points']}} points)")
    else:
        print(f"{{player_team}} was not ranked in the AP poll in {ranking_season}")
""", language="python")
        
        except Exception as e:
            st.error(f"Error loading and transforming rankings data: {e}")
            st.text(f"Exception details: {str(e)}")
            
    # Lines tab
    with transformer_tabs[5]:
        st.markdown('<div class="section-header">Lines Transformer</div>', unsafe_allow_html=True)
        
        st.markdown("""
            The Lines transformer converts betting lines data to a DataFrame.
            This tab demonstrates how to use this transformer and the resulting data structure.
        """)
        
        # Options for demonstration
        col1, col2 = st.columns(2)
        with col1:
            lines_team = st.selectbox("Select Team", options=teams if teams else ["Duke", "North Carolina", "Kentucky"], key="lines_team")
        with col2:
            lines_season = st.selectbox("Select Season", options=list(range(2024, 2010, -1)), index=0, key="lines_season")
        
        try:
            with st.spinner("Loading betting lines data..."):
                # Get betting lines data
                lines_data = client.lines.get_lines(team=lines_team, season=lines_season)
                
                if lines_data:
                    # Raw data vs transformed data
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown('<div class="subsection-header">Raw API Response (sample)</div>', unsafe_allow_html=True)
                        with st.expander("View Raw Data", expanded=True):
                            if hasattr(lines_data[0], 'get_raw_data'):
                                st.json(lines_data[0].get_raw_data())
                            else:
                                st.json(lines_data[0])
                    
                    with col2:
                        st.markdown('<div class="subsection-header">Transformed DataFrame</div>', unsafe_allow_html=True)
                        
                        # Transform to DataFrame
                        lines_df = client.transformers.lines_to_dataframe(lines_data)
                        
                        # Display the DataFrame
                        st.dataframe(lines_df, use_container_width=True)
                
                # Data Analysis
                if lines_data and not lines_df.empty:
                    st.markdown('<div class="subsection-header">Data Analysis with Transformed DataFrame</div>', unsafe_allow_html=True)
                    
                    # Show summary statistics
                    st.markdown("#### Spread and Over/Under Statistics")
                    
                    # Calculate statistics
                    spread_stats = lines_df['spread'].describe()
                    ou_stats = lines_df['over_under'].describe()
                    
                    # Display side by side
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Spread Statistics**")
                        st.write(spread_stats)
                    
                    with col2:
                        st.markdown("**Over/Under Statistics**")
                        st.write(ou_stats)
                    
                    # Create visualizations
                    st.markdown("#### Spread Distribution")
                    
                    # Create spread histogram
                    spread_chart = alt.Chart(lines_df).mark_bar().encode(
                        x=alt.X('spread:Q', bin=True, title='Spread'),
                        y=alt.Y('count()', title='Games'),
                        tooltip=['count()']
                    ).properties(
                        width=600,
                        height=300,
                        title=f"Spread Distribution for {lines_team} Games ({lines_season})"
                    )
                    
                    st.altair_chart(spread_chart, use_container_width=True)
                    
                    # Create over/under histogram
                    st.markdown("#### Over/Under Distribution")
                    
                    ou_chart = alt.Chart(lines_df).mark_bar().encode(
                        x=alt.X('over_under:Q', bin=True, title='Over/Under'),
                        y=alt.Y('count()', title='Games'),
                        tooltip=['count()']
                    ).properties(
                        width=600,
                        height=300,
                        title=f"Over/Under Distribution for {lines_team} Games ({lines_season})"
                    )
                    
                    st.altair_chart(ou_chart, use_container_width=True)
                    
                    # Moneyline analysis
                    if 'home_moneyline' in lines_df.columns and 'away_moneyline' in lines_df.columns:
                        st.markdown("#### Moneyline Analysis")
                        
                        # Create team moneyline variable
                        team_ml = []
                        opponent_ml = []
                        
                        for _, row in lines_df.iterrows():
                            if row['home_team'] == lines_team:
                                team_ml.append(row['home_moneyline'])
                                opponent_ml.append(row['away_moneyline'])
                            else:
                                team_ml.append(row['away_moneyline'])
                                opponent_ml.append(row['home_moneyline'])
                        
                        # Add to DataFrame
                        ml_df = pd.DataFrame({
                            'team_moneyline': team_ml,
                            'opponent_moneyline': opponent_ml
                        })
                        
                        # Calculate favorite/underdog counts
                        favorite_count = sum(1 for ml in team_ml if ml < 0)
                        underdog_count = sum(1 for ml in team_ml if ml > 0)
                        
                        # Display stats
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Games as Favorite", favorite_count)
                        
                        with col2:
                            st.metric("Games as Underdog", underdog_count)
                        
                        # Create data for pie chart
                        pie_data = pd.DataFrame({
                            'Status': ['Favorite', 'Underdog'],
                            'Games': [favorite_count, underdog_count]
                        })
                        
                        # Create pie chart
                        if favorite_count > 0 or underdog_count > 0:
                            ml_pie = alt.Chart(pie_data).mark_arc().encode(
                                theta=alt.Theta(field="Games", type="quantitative"),
                                color=alt.Color(field="Status", type="nominal", 
                                               scale=alt.Scale(domain=['Favorite', 'Underdog'], 
                                                               range=['#00cc00', '#cc0000'])),
                                tooltip=['Status', 'Games']
                            ).properties(
                                width=400,
                                height=400,
                                title=f"Favorite vs Underdog Status for {lines_team} ({lines_season})"
                            )
                            
                            st.altair_chart(ml_pie, use_container_width=True)
                
                # Example code for this transformer
                st.markdown('<div class="subsection-header">Example Code</div>', unsafe_allow_html=True)
                
                st.code(f"""
# Get betting lines data
lines_data = client.lines.get_lines(team="{lines_team}", season={lines_season})

# Transform to DataFrame
lines_df = client.transformers.lines_to_dataframe(lines_data)

# Filter to a specific provider
if 'provider' in lines_df.columns:
    vegas_lines = lines_df[lines_df['provider'] == 'Vegas']
    print(f"Vegas lines for {{len(vegas_lines)}} games")

# Calculate average spread and over/under
if not lines_df.empty:
    print(f"Average spread: {{lines_df['spread'].mean():.1f}}")
    print(f"Average over/under: {{lines_df['over_under'].mean():.1f}}")
    
    # Split into home and away games
    home_games = lines_df[lines_df['home_team'] == '{lines_team}']
    away_games = lines_df[lines_df['away_team'] == '{lines_team}']
    
    print(f"Home games: {{len(home_games)}}, Avg spread: {{home_games['spread'].mean():.1f}}")
    print(f"Away games: {{len(away_games)}}, Avg spread: {{away_games['spread'].mean():.1f}}")
    
    # Count games as favorite vs underdog
    fav_games = lines_df[lines_df['spread'] < 0]
    dog_games = lines_df[lines_df['spread'] > 0]
    
    print(f"Games as favorite: {{len(fav_games)}}")
    print(f"Games as underdog: {{len(dog_games)}}")
""", language="python")
        
        except Exception as e:
            st.error(f"Error loading and transforming betting lines data: {e}")
            st.text(f"Exception details: {str(e)}")
    
    # Advanced Utilities tab
    with transformer_tabs[6]:
        st.markdown('<div class="section-header">Advanced DataFrame Utilities</div>', unsafe_allow_html=True)
        
        st.markdown("""
            The CBBD SDK provides advanced utilities for working with transformed DataFrames.
            This tab demonstrates how these utilities can be used to prepare data for visualization and analysis.
        """)
        
        # Example dataset selection
        dataset_choice = st.selectbox(
            "Select Example Dataset",
            options=["Player Stats", "Team Stats", "Games Schedule", "Rankings"],
            index=0,
            key="utilities_dataset"
        )
        
        try:
            with st.spinner(f"Loading {dataset_choice} data..."):
                # Get data based on choice
                if dataset_choice == "Player Stats":
                    # Get player stats
                    util_team = st.selectbox("Select Team", options=teams if teams else ["Duke", "North Carolina", "Kentucky"], key="util_team")
                    util_season = st.selectbox("Select Season", options=list(range(2024, 2010, -1)), index=0, key="util_season")
                    
                    raw_data = client.stats.get_player_stats(team=util_team, season=util_season)
                    df = client.transformers.player_stats_to_dataframe(raw_data)
                    
                    st.markdown("#### Player Stats Dataset")
                    st.dataframe(df, use_container_width=True)
                    
                    # Utility: make_visualization_ready
                    st.markdown('<div class="subsection-header">make_visualization_ready()</div>', unsafe_allow_html=True)
                    
                    st.markdown("""
                        This utility prepares a DataFrame for visualization by ensuring all columns have the proper data types.
                        It converts numeric columns to float/int, categorical columns to categories, and date columns to datetime.
                    """)
                    
                    # Numeric and categorical columns
                    numeric_cols = [
                        'games', 'starts', 'minutes', 'points', 'turnovers', 'fouls', 
                        'assists', 'steals', 'blocks', 'usage', 'offensive_rating', 'defensive_rating'
                    ]
                    
                    categorical_cols = ['position', 'team', 'conference']
                    
                    # Make visualization ready
                    viz_df = client.transformers.utils.make_visualization_ready(
                        df,
                        numeric_columns=numeric_cols,
                        categorical_columns=categorical_cols
                    )
                    
                    st.code("""
# Make DataFrame ready for visualization
viz_df = client.transformers.utils.make_visualization_ready(
    df,
    numeric_columns=['games', 'starts', 'minutes', 'points', 'turnovers', 'fouls', 
                    'assists', 'steals', 'blocks', 'usage', 'offensive_rating', 'defensive_rating'],
    categorical_columns=['position', 'team', 'conference']
)
                    """, language="python")
                    
                    # Utility: add_calculated_columns
                    st.markdown('<div class="subsection-header">add_calculated_columns()</div>', unsafe_allow_html=True)
                    
                    st.markdown("""
                        This utility adds calculated columns to a DataFrame based on provided functions.
                        It's useful for derived metrics like per-game statistics or efficiency ratings.
                    """)
                    
                    # Calculated columns
                    calculations = {
                        'points_per_game': lambda df: df['points'] / df['games'],
                        'rebounds_per_game': lambda df: df['rebounds'] / df['games'] if 'rebounds' in df.columns else None,
                        'assists_per_game': lambda df: df['assists'] / df['games'],
                        'efficiency': lambda df: (df['points'] + df['rebounds'] + df['assists'] - df['turnovers']) / df['minutes'] 
                                               if all(col in df.columns for col in ['rebounds', 'minutes']) else None
                    }
                    
                    # Add calculated columns
                    calc_df = client.transformers.utils.add_calculated_columns(viz_df, calculations)
                    
                    # Display the result
                    st.dataframe(calc_df[[
                        'name', 'position', 'games', 
                        'points_per_game', 'rebounds_per_game', 'assists_per_game', 'efficiency'
                    ]].sort_values('points_per_game', ascending=False), use_container_width=True)
                    
                    st.code("""
# Add calculated columns
calculations = {
    'points_per_game': lambda df: df['points'] / df['games'],
    'rebounds_per_game': lambda df: df['rebounds'] / df['games'],
    'assists_per_game': lambda df: df['assists'] / df['games'],
    'efficiency': lambda df: (df['points'] + df['rebounds'] + df['assists'] - df['turnovers']) / df['minutes']
}

calc_df = client.transformers.utils.add_calculated_columns(viz_df, calculations)
                    """, language="python")
                    
                    # Create a visualization with the processed data
                    st.markdown('<div class="subsection-header">Visualization Example</div>', unsafe_allow_html=True)
                    
                    # Sort by points per game and get top players
                    top_players = calc_df.sort_values('points_per_game', ascending=False).head(8)
                    
                    # Create a scatter plot
                    if 'efficiency' in top_players.columns and not top_players['efficiency'].isna().all():
                        scatter = alt.Chart(top_players).mark_circle(size=100).encode(
                            x=alt.X('points_per_game:Q', title='Points Per Game'),
                            y=alt.Y('efficiency:Q', title='Efficiency'),
                            color=alt.Color('position:N', title='Position'),
                            tooltip=['name', 'position', 'points_per_game', 'rebounds_per_game', 'assists_per_game', 'efficiency']
                        ).properties(
                            width=700,
                            height=500,
                            title=f"Efficiency vs Scoring for {util_team} Players ({util_season})"
                        )
                        
                        st.altair_chart(scatter, use_container_width=True)
                
                # Example code for all utilities
                st.markdown('<div class="subsection-header">Complete Example</div>', unsafe_allow_html=True)
                
                st.code("""
# Get the data
player_stats = client.stats.get_player_stats(team="Duke", season=2023)
df = client.transformers.player_stats_to_dataframe(player_stats)

# Access the utilities
utils = client.transformers.utils

# 1. Make visualization ready
viz_df = utils.make_visualization_ready(
    df,
    numeric_columns=['games', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers'],
    categorical_columns=['position', 'team', 'conference'],
    date_columns=['game_date']  # If present
)

# 2. Add calculated columns
calculations = {
    'pts_per_game': lambda df: df['points'] / df['games'],
    'ast_per_game': lambda df: df['assists'] / df['games'],
    'reb_per_game': lambda df: df['rebounds'] / df['games'] if 'rebounds' in df.columns else None,
    'stl_per_game': lambda df: df['steals'] / df['games'],
    'blk_per_game': lambda df: df['blocks'] / df['games'],
    'to_per_game': lambda df: df['turnovers'] / df['games'],
    'efficiency': lambda df: (df['points'] + df['assists']*2 + df['rebounds'] + 
                             df['steals']*2 + df['blocks']*2 - df['turnovers']) / df['games']
}

players_with_metrics = utils.add_calculated_columns(viz_df, calculations)

# 3. Filter to a specific season
if 'season' in players_with_metrics.columns:
    season_data = utils.filter_season(players_with_metrics, 2023)

# 4. Filter to a specific team
if 'team' in players_with_metrics.columns:
    team_data = utils.filter_team(players_with_metrics, "Duke")

# 5. Standardize column names
std_df = utils.standardize_column_names(players_with_metrics)

# Now the DataFrame is ready for analysis and visualization
top_performers = players_with_metrics.sort_values('efficiency', ascending=False).head(10)
print(top_performers[['name', 'position', 'pts_per_game', 'reb_per_game', 'ast_per_game', 'efficiency']])
                """, language="python")
                
            
        except Exception as e:
            st.error(f"Error demonstrating utilities: {e}")
            st.text(f"Exception details: {str(e)}")
    
elif page == "Advanced Analysis" and client:
    st.markdown('<div class="main-header">Advanced Analysis</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Team Season Profile", "Player Season Profile", "Game Analysis"])
    
    with tab1:
        try:
            with st.spinner(f"Loading team season profile for {team} ({season})..."):
                profile = client.advanced.team_season.get_profile(team=team, season=season)
                
                if profile:
                    st.markdown(f"### Team Profile for {team} ({season})")
                    
                    # Basic team info
                    st.markdown('<div class="subsection-header">Team Information</div>', unsafe_allow_html=True)
                    
                    if 'team' in profile and profile['team']:
                        st.json(profile['team'])
                    
                    # Roster summary
                    st.markdown('<div class="subsection-header">Roster Summary</div>', unsafe_allow_html=True)
                    
                    if 'roster' in profile and profile['roster'] and 'players' in profile['roster']:
                        roster_df = pd.DataFrame(profile['roster']['players'])
                        st.dataframe(roster_df)
                    
                    # Games summary
                    st.markdown('<div class="subsection-header">Games Summary</div>', unsafe_allow_html=True)
                    
                    if 'games' in profile and profile['games']:
                        games_df = pd.DataFrame(profile['games'])
                        
                        # Calculate and display record
                        wins = len([g for g in profile['games'] if 
                                    (g.get('home_team') == team and g.get('home_winner')) or 
                                    (g.get('away_team') == team and g.get('away_winner'))])
                        
                        losses = len([g for g in profile['games'] if 
                                     (g.get('home_team') == team and not g.get('home_winner')) or 
                                     (g.get('away_team') == team and not g.get('away_winner'))])
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Record", f"{wins}-{losses}")
                        
                        with col2:
                            win_pct = wins / (wins + losses) if (wins + losses) > 0 else 0
                            st.metric("Win %", f"{win_pct:.1%}")
                        
                        st.dataframe(games_df)
                    
                    # Rankings history
                    st.markdown('<div class="subsection-header">Rankings History</div>', unsafe_allow_html=True)
                    
                    if 'rankings' in profile and profile['rankings']:
                        rankings_df = pd.DataFrame(profile['rankings'])
                        
                        chart = alt.Chart(rankings_df).mark_line(point=True).encode(
                            x="week:O",
                            y=alt.Y("rank:Q", scale=alt.Scale(reverse=True)),
                            color="poll:N",
                            tooltip=["week", "poll", "rank"]
                        ).properties(
                            title=f"Rankings History for {team} ({season})",
                            width=600,
                            height=400
                        )
                        
                        st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning(f"No team season profile found for {team} in {season}.")
        except Exception as e:
            st.error(f"Error loading team season profile: {e}")
    
    with tab2:
        st.markdown("### Player Season Profile")
        
        # Get player ID
        player_id = st.number_input("Player ID", min_value=1, value=1000, step=1)
        
        if player_id:
            try:
                with st.spinner(f"Loading player season profile (ID: {player_id}, Season: {season})..."):
                    profile = client.advanced.player_season.get_profile(player_id=player_id, season=season)
                    
                    if profile:
                        st.markdown(f"### Player Profile (ID: {player_id}, Season: {season})")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown('<div class="subsection-header">Player Information</div>', unsafe_allow_html=True)
                            st.json({
                                "player_id": profile['player_id'],
                                "season": profile['season'],
                                "team": profile['team']
                            })
                        
                        # Season stats summary
                        st.markdown('<div class="subsection-header">Season Stats</div>', unsafe_allow_html=True)
                        
                        if 'season_stats' in profile and profile['season_stats']:
                            stats_df = pd.DataFrame(profile['season_stats'])
                            st.dataframe(stats_df)
                        
                        # Game stats
                        st.markdown('<div class="subsection-header">Game Stats</div>', unsafe_allow_html=True)
                        
                        if 'game_stats' in profile and profile['game_stats']:
                            game_stats_df = pd.DataFrame(profile['game_stats'])
                            
                            # Create a points by game chart
                            if 'points' in game_stats_df.columns:
                                chart = alt.Chart(game_stats_df).mark_bar().encode(
                                    x=alt.X("game_id:O", title="Game"),
                                    y=alt.Y("points:Q", title="Points"),
                                    color=alt.Color("points:Q", scale=alt.Scale(scheme="blues")),
                                    tooltip=["game_id", "opponent", "points", "minutes"]
                                ).properties(
                                    title="Points by Game",
                                    width=600,
                                    height=300
                                )
                                
                                st.altair_chart(chart, use_container_width=True)
                            
                            st.dataframe(game_stats_df)
                    else:
                        st.warning(f"No player season profile found for player ID {player_id} in {season}.")
            except Exception as e:
                st.error(f"Error loading player season profile: {e}")
    
    with tab3:
        st.markdown("### Game Analysis")
        
        # Get game ID
        game_id = st.number_input("Game ID", min_value=1, value=400000, step=1)
        
        if game_id:
            try:
                with st.spinner(f"Loading game analysis (ID: {game_id})..."):
                    analysis = client.advanced.game_analysis.get_game_analysis(game_id=game_id)
                    
                    if analysis:
                        # Game info
                        st.markdown('<div class="subsection-header">Game Information</div>', unsafe_allow_html=True)
                        
                        if 'game' in analysis:
                            game_info = analysis['game']
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Home Team", game_info.get('home_team', ''))
                                st.metric("Home Score", game_info.get('home_points', ''))
                            
                            with col2:
                                st.metric("Away Team", game_info.get('away_team', ''))
                                st.metric("Away Score", game_info.get('away_points', ''))
                            
                            with col3:
                                st.metric("Date", game_info.get('start_date', ''))
                                st.metric("Venue", game_info.get('venue', ''))
                        
                        # Team stats
                        st.markdown('<div class="subsection-header">Team Stats</div>', unsafe_allow_html=True)
                        
                        if 'team_stats' in analysis and analysis['team_stats']:
                            team_stats_df = pd.DataFrame(analysis['team_stats'])
                            st.dataframe(team_stats_df)
                        
                        # Key plays
                        st.markdown('<div class="subsection-header">Key Plays</div>', unsafe_allow_html=True)
                        
                        if 'key_plays' in analysis and analysis['key_plays']:
                            key_plays_df = pd.DataFrame(analysis['key_plays'])
                            st.dataframe(key_plays_df)
                        
                        # Play distribution
                        st.markdown('<div class="subsection-header">Play Distribution</div>', unsafe_allow_html=True)
                        
                        if 'play_distribution' in analysis and analysis['play_distribution']:
                            play_dist = analysis['play_distribution']
                            play_dist_df = pd.DataFrame({
                                "Play Type": list(play_dist.keys()),
                                "Count": list(play_dist.values())
                            })
                            
                            chart = alt.Chart(play_dist_df).mark_bar().encode(
                                x=alt.X("Count:Q"),
                                y=alt.Y("Play Type:N", sort="-x"),
                                color=alt.Color("Count:Q", scale=alt.Scale(scheme="blues")),
                                tooltip=["Play Type", "Count"]
                            ).properties(
                                title="Play Type Distribution",
                                width=600,
                                height=400
                            )
                            
                            st.altair_chart(chart, use_container_width=True)
                    else:
                        st.warning(f"No game analysis found for game ID {game_id}.")
            except Exception as e:
                st.error(f"Error loading game analysis: {e}")

elif page == "Rankings" and client:
    st.markdown('<div class="main-header">Rankings</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Add season selector (separate from the global sidebar one)
        rankings_season = st.selectbox(
            "Season", 
            list(range(2025, 2010, -1)),
            index=0,
            key="rankings_season"
        )
    
    with col2:
        # Add week selector
        week = st.slider("Week", min_value=1, max_value=20, value=5)
    
    with col3:
        # Add poll type selector
        poll_type = st.selectbox("Poll Type", ["ap", "coaches"])
    
    # Add a button to find available data
    find_data = st.button("Find Available Rankings Data")
    
    if find_data:
        st.write("Checking for available rankings data across seasons...")
        available_data = {}
        
        # Check a few seasons and weeks
        for s in [2022, 2023, 2024]:
            available_data[s] = {}
            for w in [1, 5, 10, 15]:
                try:
                    with st.spinner(f"Checking season {s}, week {w}..."):
                        data = client.rankings.get_rankings(season=s, week=w, poll_type=poll_type)
                        has_data = len(data) > 0 and any(len(r.polls) > 0 for r in data)
                        available_data[s][w] = "✅" if has_data else "❌"
                except Exception as e:
                    available_data[s][w] = f"❌ (Error: {str(e)})"
        
        # Display results
        results_df = pd.DataFrame(available_data)
        results_df.index.name = "Week"
        st.write("Available Rankings Data:")
        st.dataframe(results_df)
    
    try:
        with st.spinner(f"Loading rankings data for season {rankings_season}, week {week}..."):
            rankings_data = client.rankings.get_rankings(
                season=rankings_season, 
                week=week, 
                poll_type=poll_type
            )
            
            if rankings_data:
                # Show a sample of the raw data in expandable section
                with st.expander("Raw Data Sample"):
                    if len(rankings_data) > 0:
                        if hasattr(rankings_data[0], 'get_raw_data'):
                            st.json(rankings_data[0].get_raw_data())
                        else:
                            # If get_raw_data is not available, try to get the dictionary representation
                            try:
                                st.json(rankings_data[0].__dict__.get('_data', {}))
                            except:
                                st.write("Raw data not available")
                        
                        # Also show a sample poll if available
                        if hasattr(rankings_data[0], 'polls') and len(rankings_data[0].polls) > 0:
                            st.subheader("Sample Poll Data")
                            poll = rankings_data[0].polls[0]
                            if hasattr(poll, 'get_raw_data'):
                                st.json(poll.get_raw_data())
                            else:
                                try:
                                    st.json(poll.__dict__.get('_data', {}))
                                except:
                                    st.write("Raw poll data not available")
                
                # Debug information
                st.text(f"API Response Type: {type(rankings_data)}")
                st.text(f"API Response Length: {len(rankings_data) if rankings_data else 0}")
                
                # Extract all ranks from all polls
                all_ranks = []
                for ranking in rankings_data:
                    # Debug each ranking
                    st.text(f"Processing ranking: season={ranking.season}, week={ranking.week}, polls={len(ranking.polls) if hasattr(ranking, 'polls') else 'No polls'}")
                    
                    for poll in ranking.polls:
                        st.text(f"Poll: {poll.poll}, type={poll.poll_type}, ranks={len(poll.ranks)}")
                        
                        # Add debug for poll type comparison
                        st.text(f"Poll type comparison: '{poll.poll_type}' == '{poll_type}' is {poll.poll_type and poll.poll_type.lower() == poll_type.lower()}")
                        
                        # First try with the normal filter
                        ranks_added = False
                        if poll.poll_type and poll.poll_type.lower() == poll_type.lower():
                            for rank in poll.ranks:
                                all_ranks.append({
                                    "Rank": rank.rank,
                                    "Team": rank.school,
                                    "Conference": rank.conference,
                                    "Points": rank.points,
                                    "First Place Votes": rank.first_place_votes
                                })
                            ranks_added = True
                        
                        # If no ranks were added but this is an AP poll and we requested AP, try using the name
                        if not ranks_added and poll_type.lower() == "ap" and poll.poll and "AP" in poll.poll:
                            st.text(f"Using fallback AP poll matching")
                            for rank in poll.ranks:
                                all_ranks.append({
                                    "Rank": rank.rank,
                                    "Team": rank.school,
                                    "Conference": rank.conference,
                                    "Points": rank.points,
                                    "First Place Votes": rank.first_place_votes
                                })
                
                # Add debug for all_ranks length
                st.text(f"Extracted {len(all_ranks)} rankings in total")
                
                if all_ranks:
                    # Convert to DataFrame for better display
                    rankings_df = pd.DataFrame(all_ranks)
                    st.dataframe(rankings_df)
                    
                    # Visualization of top 25
                    top25 = rankings_df.nsmallest(25, "Rank")
                    
                    chart = alt.Chart(top25).mark_bar().encode(
                        y=alt.Y("Team:N", sort="x"),
                        x=alt.X("Rank:Q", scale=alt.Scale(reverse=True)),
                        color=alt.Color("Conference:N"),
                        tooltip=["Rank", "Team", "Conference", "Points", "First Place Votes"]
                    ).properties(
                        title=f"{poll_type.upper()} Poll - Week {week}, Season {rankings_season}",
                        width=600,
                        height=500
                    )
                    
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning(f"No rankings found for poll type {poll_type} in week {week} of season {rankings_season}.")
            else:
                st.warning(f"No rankings data found for season {rankings_season}, week {week}.")
    except Exception as e:
        st.error(f"Error loading rankings data: {e}")
        # Print the full exception traceback
        import traceback
        st.text(traceback.format_exc())

elif page == "Ratings" and client:
    st.markdown('<div class="main-header">Ratings</div>', unsafe_allow_html=True)
    
    # Add rating type selector
    rating_type = st.selectbox("Rating Type", ["SRS", "Adjusted Efficiency"])
    
    try:
        with st.spinner(f"Loading ratings data for season {season}..."):
            if rating_type == "SRS":
                ratings_data = client.ratings.get_srs_ratings(
                    season=season,
                    conference=conference if conference != "All" else None,
                    team=team if team != "All" else None
                )
                
                if ratings_data:
                    # Show a sample of the raw data in expandable section
                    with st.expander("Raw Data Sample"):
                        if len(ratings_data) > 0:
                            if hasattr(ratings_data[0], 'get_raw_data'):
                                st.json(ratings_data[0].get_raw_data())
                            else:
                                # If get_raw_data is not available, try to get the dictionary representation
                                try:
                                    st.json(ratings_data[0].__dict__.get('_data', {}))
                                except:
                                    st.write("Raw data not available")
                    
                    # Convert to DataFrame for better display
                    ratings_df = pd.DataFrame([
                        {
                            "Team": rating.team,
                            "Conference": rating.conference,
                            "Rating": rating.rating
                        } for rating in ratings_data
                    ])
                    
                    st.dataframe(ratings_df)
                    
                    # Visualization
                    chart = alt.Chart(ratings_df).mark_bar().encode(
                        y=alt.Y("Team:N", sort="-x"),
                        x=alt.X("Rating:Q"),
                        color=alt.Color("Conference:N"),
                        tooltip=["Team", "Conference", "Rating"]
                    ).properties(
                        title=f"SRS Ratings - Season {season}",
                        width=600,
                        height=500
                    )
                    
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning(f"No SRS ratings data found for season {season}.")
            
            elif rating_type == "Adjusted Efficiency":
                ratings_data = client.ratings.get_adjusted_efficiency(
                    season=season,
                    conference=conference if conference != "All" else None,
                    team=team if team != "All" else None
                )
                
                if ratings_data:
                    # Show a sample of the raw data in expandable section
                    with st.expander("Raw Data Sample"):
                        if len(ratings_data) > 0:
                            if hasattr(ratings_data[0], 'get_raw_data'):
                                st.json(ratings_data[0].get_raw_data())
                            else:
                                # If get_raw_data is not available, try to get the dictionary representation
                                try:
                                    st.json(ratings_data[0].__dict__.get('_data', {}))
                                except:
                                    st.write("Raw data not available")
                    
                    # Convert to DataFrame for better display
                    ratings_df = pd.DataFrame([
                        {
                            "Team": rating.team,
                            "Conference": rating.conference,
                            "Offensive Rating": rating.offensive_rating,
                            "Defensive Rating": rating.defensive_rating,
                            "Net Rating": rating.net_rating
                        } for rating in ratings_data
                    ])
                    
                    st.dataframe(ratings_df)
                    
                    # Visualization
                    chart = alt.Chart(ratings_df).mark_circle(size=60).encode(
                        x=alt.X("Offensive Rating:Q", title="Offensive Rating"),
                        y=alt.Y("Defensive Rating:Q", title="Defensive Rating", scale=alt.Scale(reverse=True)),
                        color=alt.Color("Conference:N"),
                        tooltip=["Team", "Conference", "Offensive Rating", "Defensive Rating", "Net Rating"]
                    ).properties(
                        title=f"Adjusted Efficiency Ratings - Season {season}",
                        width=600,
                        height=500
                    )
                    
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning(f"No adjusted efficiency ratings data found for season {season}.")
            
    except Exception as e:
        st.error(f"Error loading ratings data: {e}")

elif page == "Plays" and client:
    st.markdown('<div class="main-header">Plays</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["By Game", "By Team", "Debug"])
    
    with tab1:
        # Game ID input
        game_id = st.number_input("Game ID", min_value=1, value=401000, step=1)
        
        # Option to filter by shooting plays only
        shooting_plays_only = st.checkbox("Shooting Plays Only", value=False)
        
        if game_id:
            try:
                with st.spinner(f"Loading plays data for game ID {game_id}..."):
                    plays_data = client.plays.get_plays(
                        game_id=game_id,
                        shooting_plays_only=shooting_plays_only
                    )
                    
                    if plays_data and len(plays_data) > 0:
                        # Show a sample of the raw data in expandable section
                        with st.expander("Raw Data Sample"):
                            if hasattr(plays_data[0], 'get_raw_data'):
                                st.json(plays_data[0].get_raw_data())
                            else:
                                st.write("Raw data method not available")
                        
                        # Convert to DataFrame for better display
                        plays_df = pd.DataFrame([
                            {
                                "Game ID": play.game_id,
                                "Period": play.period,
                                "Clock": play.clock,
                                "Team": play.team,
                                "Player": play.player,
                                "Play Type": play.play_type,
                                "Home Score": play.home_score,
                                "Away Score": play.away_score,
                                "Description": play.play_text or play.description
                            } for play in plays_data
                        ])
                        
                        # Remove columns that are all None
                        for col in plays_df.columns:
                            if plays_df[col].isna().all() or (plays_df[col] == 'None').all():
                                plays_df = plays_df.drop(col, axis=1)
                        
                        st.dataframe(plays_df)
                        
                        # Play type distribution - check if we have data for this
                        key_for_chart = next((col for col in ["Play Type", "event_type"] if col in plays_df.columns), None)
                        
                        if key_for_chart and not plays_df[key_for_chart].isna().all() and not (plays_df[key_for_chart] == 'None').all():
                            play_type_counts = plays_df[key_for_chart].value_counts().reset_index()
                            play_type_counts.columns = [key_for_chart, "Count"]
                            
                            chart = alt.Chart(play_type_counts).mark_bar().encode(
                                y=alt.Y(f"{key_for_chart}:N", sort="-x"),
                                x=alt.X("Count:Q"),
                                tooltip=[key_for_chart, "Count"]
                            ).properties(
                                title=f"Play Type Distribution - Game ID {game_id}",
                                width=600,
                                height=400
                            )
                            
                            st.altair_chart(chart, use_container_width=True)
                    else:
                        st.warning(f"No plays data found for game ID {game_id}.")
            except Exception as e:
                st.error(f"Error loading plays data: {e}")
                import traceback
                st.text(traceback.format_exc())
    
    with tab2:
        # Option to filter by shooting plays only
        shooting_plays_only_team = st.checkbox("Shooting Plays Only", value=False, key="shooting_plays_team")
        
        try:
            with st.spinner(f"Loading plays data for {team} in season {season}..."):
                plays_data = client.plays.get_plays_by_team(
                    team=team,
                    season=season,
                    shooting_plays_only=shooting_plays_only_team
                )
                
                if plays_data and len(plays_data) > 0:
                    # Show a sample of the raw data in expandable section
                    with st.expander("Raw Data Sample"):
                        if hasattr(plays_data[0], 'get_raw_data'):
                            st.json(plays_data[0].get_raw_data())
                        else:
                            st.write("Raw data method not available")
                    
                    # Convert to DataFrame for better display
                    plays_df = pd.DataFrame([
                        {
                            "Game ID": play.game_id,
                            "Period": play.period,
                            "Clock": play.clock,
                            "Team": play.team,
                            "Player": play.player,
                            "Play Type": play.play_type,
                            "Home Score": play.home_score,
                            "Away Score": play.away_score,
                            "Description": play.play_text or play.description,
                            "Scoring Play": play.scoring_play,
                            "Shooting Play": play.shooting_play
                        } for play in plays_data
                    ])
                    
                    # Remove columns that are all None
                    for col in plays_df.columns:
                        if plays_df[col].isna().all() or (plays_df[col] == 'None').all():
                            plays_df = plays_df.drop(col, axis=1)
                    
                    st.dataframe(plays_df)
                    
                    # Play type distribution - check if we have data for this
                    key_for_chart = next((col for col in ["Play Type", "event_type"] if col in plays_df.columns), None)
                    
                    if key_for_chart and not plays_df[key_for_chart].isna().all() and not (plays_df[key_for_chart] == 'None').all():
                        play_type_counts = plays_df[key_for_chart].value_counts().reset_index()
                        play_type_counts.columns = [key_for_chart, "Count"]
                        
                        chart = alt.Chart(play_type_counts).mark_bar().encode(
                            y=alt.Y(f"{key_for_chart}:N", sort="-x"),
                            x=alt.X("Count:Q"),
                            tooltip=[key_for_chart, "Count"]
                        ).properties(
                            title=f"Play Type Distribution for {team} - Season {season}",
                            width=600,
                            height=400
                        )
                        
                        st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning(f"No plays data found for {team} in season {season}.")
        except Exception as e:
            st.error(f"Error loading plays data: {e}")
            import traceback
            st.text(traceback.format_exc())
    
    with tab3:
        st.markdown("### Play Data Debug")
        st.write("""
        This tab helps diagnose issues with the Plays API data.
        """)
        
        debug_game_id = st.number_input("Game ID for Debug", min_value=1, value=401583, step=1)
        
        if st.button("Check API Data Structure"):
            try:
                plays_data = client.plays.get_plays(
                    game_id=debug_game_id,
                    shooting_plays_only=False
                )
                
                if plays_data and len(plays_data) > 0:
                    st.success(f"Found {len(plays_data)} plays for game ID {debug_game_id}")
                    
                    # Show the raw data for the first play
                    st.subheader("First Play Raw Data")
                    if hasattr(plays_data[0], 'get_raw_data'):
                        raw_data = plays_data[0].get_raw_data()
                        st.json(raw_data)
                        
                        # Check available fields
                        st.subheader("Available Fields")
                        st.write(", ".join(raw_data.keys()))
                        
                        # Check specific important fields
                        st.subheader("Important Field Values")
                        for field in ['id', 'gameId', 'playType', 'team', 'period', 'clock']:
                            st.write(f"{field}: {raw_data.get(field, 'Not available')}")
                    else:
                        st.warning("Raw data method not available on Play objects")
                else:
                    st.warning(f"No plays data found for game ID {debug_game_id}")
            except Exception as e:
                st.error(f"Error checking API data: {e}")
                import traceback
                st.text(traceback.format_exc())

elif page == "Lines" and client:
    st.markdown('<div class="main-header">Betting Lines</div>', unsafe_allow_html=True)
    
    try:
        with st.spinner(f"Loading betting lines data for {team} in season {season}..."):
            lines_data = client.lines.get_lines(
                season=season,
                team=team
            )
            
            if lines_data:
                # Show a sample of the raw data in expandable section
                with st.expander("Raw Data Sample"):
                    if len(lines_data) > 0:
                        if hasattr(lines_data[0], 'get_raw_data'):
                            st.json(lines_data[0].get_raw_data())
                        else:
                            # If get_raw_data is not available, try to get the dictionary representation
                            try:
                                st.json(lines_data[0].__dict__.get('_data', {}))
                            except:
                                st.write("Raw data not available")
                
                # Convert to DataFrame for better display
                all_lines = []
                
                for line in lines_data:
                    all_lines.append({
                        "Game ID": line.game_id,
                        "Date": getattr(line, 'start_date', None),
                        "Home Team": line.home_team,
                        "Away Team": line.away_team,
                        "Provider": line.provider,
                        "Spread": line.spread,
                        "Over/Under": line.over_under,
                        "Home Moneyline": line.home_moneyline,
                        "Away Moneyline": line.away_moneyline
                    })
                
                if all_lines:
                    lines_df = pd.DataFrame(all_lines)
                    st.dataframe(lines_df)
                    
                    # Spread distribution
                    if len(lines_df) > 0 and "Spread" in lines_df.columns:
                        # Filter out any potential NaN values
                        spread_df = lines_df[lines_df["Spread"].notna()]
                        
                        if not spread_df.empty:
                            hist = alt.Chart(spread_df).mark_bar().encode(
                                x=alt.X("Spread:Q", bin=True),
                                y="count()",
                                tooltip=["count()", "Spread:Q"]
                            ).properties(
                                title=f"Spread Distribution - Season {season}",
                                width=600,
                                height=300
                            )
                            
                            st.altair_chart(hist, use_container_width=True)
                    
                    # Over/Under distribution
                    if len(lines_df) > 0 and "Over/Under" in lines_df.columns:
                        # Filter out any potential NaN values
                        ou_df = lines_df[lines_df["Over/Under"].notna()]
                        
                        if not ou_df.empty:
                            hist = alt.Chart(ou_df).mark_bar().encode(
                                x=alt.X("Over/Under:Q", bin=True),
                                y="count()",
                                tooltip=["count()", "Over/Under:Q"]
                            ).properties(
                                title=f"Over/Under Distribution - Season {season}",
                                width=600,
                                height=300
                            )
                            
                            st.altair_chart(hist, use_container_width=True)
                else:
                    st.warning(f"No lines details found for {team} in season {season}.")
            else:
                st.warning(f"No betting lines data found for {team} in season {season}.")
    except Exception as e:
        st.error(f"Error loading betting lines data: {e}")
        import traceback
        st.text(traceback.format_exc())

else:
    if page != "Home":
        st.warning("Please enter a valid API key to use this page.") 