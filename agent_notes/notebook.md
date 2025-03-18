# Development Notebook

## 2023-07-20: Project Setup and Initial Research

- Created project folder structure
- Researched CFBD API documentation
- Explored API capabilities using Perplexity and Firecrawl
- Analyzed existing implementations
- Decided on SDK architecture and structure
- Established naming conventions and coding standards

## 2023-07-21: Core Implementation

- Implemented base client class
- Added authentication handling
- Implemented error handling and retries
- Added caching functionality
- Created utility functions
- Implemented first set of API wrappers (Teams, Conferences, Games)

## 2023-07-22: API Implementation

- Implemented Stats API
- Implemented Rankings API
- Implemented Ratings API
- Implemented Plays API
- Created corresponding model classes
- Added validation and type checking

## 2023-07-23: Advanced Features

- Implemented Lines API
- Implemented Lineups API
- Added advanced functionality combining multiple endpoints
- Created Team Season Profile
- Created Player Season Profile
- Created Game Analysis

## 2023-07-24: Additional APIs

- Implemented Draft API
- Implemented Recruiting API
- Implemented Substitutions API
- Enhanced error handling
- Added additional validation

## 2023-07-25: Testing and Documentation

- Created mock responses for API testing
- Set up test framework
- Added logging configuration
- Created setup.py for package distribution
- Updated requirements.txt

## 2023-07-26: Streamlit App and Examples

- Created Streamlit app for SDK demonstration
- Built interactive UI with visualizations
- Added example scripts
- Prepared for PyPI distribution

## Key Decisions

1. **API Structure**:
   - Use a client-based approach with property access to API modules
   - Organize endpoints by logical domain (Teams, Games, Stats, etc.)
   - Implement advanced functionality as combinations of multiple endpoints

2. **Model Design**:
   - Use proper Python classes for model objects
   - Implement property-based access for clean interface
   - Use type hints for better IDE support
   - Include validation where appropriate

3. **Error Handling**:
   - Create custom exceptions for different error types
   - Implement automatic retries for transient errors
   - Provide clear error messages

4. **Caching**:
   - Implement in-memory cache with configurable TTL
   - Cache at the API method level
   - Allow users to disable caching if needed

5. **Logging**:
   - Implement configurable logging
   - Allow setting log level and destination
   - Include request and response information for debugging

6. **Testing**:
   - Create mock responses for unit testing
   - Implement integration tests for API combinations
   - Test error handling and edge cases

## Challenges and Solutions

1. **Challenge**: Handling complex nested API responses
   **Solution**: Created nested model classes with proper validation

2. **Challenge**: Managing API rate limits
   **Solution**: Implemented caching and automatic retries with backoff

3. **Challenge**: Providing a clean interface while preserving API flexibility
   **Solution**: Used optional parameters and sensible defaults

4. **Challenge**: Handling different error scenarios
   **Solution**: Created custom exceptions and comprehensive error handling

5. **Challenge**: Demonstrating SDK capabilities
   **Solution**: Created Streamlit app with interactive UI and visualizations

# CBBD Python SDK Project Notes

## Debugging and Fixing the Plays Page

### Problem Identification
- The Plays page was showing empty data with "None" values for most fields
- There were two errors:
  1. `'PlaysAPI' object has no attribute 'get_plays_by_game'` - Method name was incorrect
  2. `'Play' object has no attribute 'opponent'` - Attribute didn't exist in the model

### Solution Approach
1. Added debug logging to the API methods to see the raw API response
2. Updated the Play model to handle different field naming conventions (camelCase vs snake_case)
3. Created a "Raw Data Sample" expandable section to show the actual API response data
4. Added a Debug tab to help developers understand the API structure

### Implementation Details
- Fixed method name from `get_plays_by_game` to `get_plays`
- Updated property access in the Play model to fall back to alternative field names
- Added proper error handling with traceback display
- Removed non-existent fields from the DataFrame display
- Added fallback methods for extracting data when fields are missing

## UI Enhancements

### Raw Data Sample Feature
- Added expandable "Raw Data Sample" sections to all pages that make API calls:
  - Teams
  - Games
  - Stats
  - Rankings
  - Ratings
  - Plays
  - Lines
- This feature helps developers understand the structure of the API responses
- Implemented fallbacks when `get_raw_data()` method is not available

### Base Model Improvements
- Created a `BaseModel` class with standardized methods:
  - `get_raw_data()` for exposing the raw API response
  - `to_dict()` for converting to dictionaries
  - `__str__()` for better string representation
  - `get_base_properties()` for customizable string output

### Future Enhancements
- Consider adding model-specific debug information to each page
- Add more interactive visualizations for the data
- Improve error messages with hints for fixing common issues
- Provide links to API documentation for each endpoint

## Developer Notes

### SDK Architecture

The SDK is designed with a clean, modular architecture:

- `cbbd/client.py`: Main client class
- `cbbd/api/`: API endpoint implementations
- `cbbd/models/`: Data models for API responses
- `cbbd/advanced/`: Advanced combined endpoints
- `cbbd/utils/`: Utility functions and classes
- `cbbd/exceptions.py`: Custom exception classes
- `cbbd/constants.py`: Constants used throughout the SDK
- `cbbd/transformers/`: Data transformation utilities (new!)

### Important Patterns

1. **Lazy Loading**: API endpoint modules are loaded only when first accessed to reduce startup time and memory usage.

2. **Model Classes**: Each API response is mapped to a model class that provides a clean interface for accessing data.

3. **Raw Data Access**: All model objects provide a `get_raw_data()` method to access the original API response.

4. **Caching**: Responses can be cached to reduce API calls during a session.

5. **Logging**: Comprehensive logging is available throughout the SDK.

6. **Fluent Interface**: API methods are designed to be chainable where appropriate.

7. **Error Handling**: Custom exception classes provide detailed error information.

8. **Advanced Features**: Combined endpoints that use multiple API calls to provide enhanced functionality.

9. **Data Transformations**: Utility functions to convert API responses to pandas DataFrames (new!)

### New Data Transformation Layer

We've added a comprehensive data transformation layer to the SDK that makes working with the API data much easier. The key components include:

1. **BaseTransformer**: A base class that provides common functionality for all transformers:
   - Handling NULL values (`"NULL"` strings converted to `None`)
   - Extracting values from nested structures
   - Flattening nested dictionaries
   - Converting to numeric types safely
   - Standardized methods for all transformers

2. **Endpoint-Specific Transformers**: 
   - `RosterTransformer`: For team roster data
   - `TeamsTransformer`: For team information
   - `GamesTransformer`: For game data and box scores
   - `PlayersTransformer`: For player information and stats
   - `RankingsTransformer`: For rankings data
   - `RatingsTransformer`: For team ratings
   - `LinesTransformer`: For betting lines
   - `PlaysTransformer`: For play-by-play data

3. **DataFrameUtils**: A utility class for working with DataFrames:
   - Making DataFrames ready for visualization
   - Adding calculated columns
   - Filtering by season, team, etc.
   - Standardizing column names

4. **Client Integration**: The transformers are available through the client instance:
   ```python
   client = CBBDClient()
   # Get data from API
   roster = client.teams.get_roster(team="Duke", season=2023)
   # Transform to DataFrame
   df = client.transformers.roster_to_dataframe(roster)
   ```

### Common Challenges Addressed

The transformation layer addresses several common challenges:

1. **Nested Data**: The API often returns deeply nested structures that are hard to work with in data analysis tools. The transformers flatten these structures.

2. **NULL Values**: The API uses string "NULL" values instead of proper null values. The transformers convert these to proper None/NaN values.

3. **Inconsistent Access Patterns**: Some data needs to be accessed differently depending on the endpoint. The transformers provide a consistent interface.

4. **Type Conversion**: String values are automatically converted to appropriate types (numeric, dates, etc.).

5. **Calculated Fields**: Common calculated fields are automatically added where appropriate (e.g., experience = current_season - start_season).

### API Response Format

API responses follow these general formats:

1. **List of Objects**: Most endpoints return a list of objects with a consistent schema.

2. **Nested Objects**: Some endpoints return objects with nested objects (e.g., games with home and away teams).

3. **Paginated Responses**: Some endpoints support pagination.

4. **Null Values**: The API uses the string "NULL" to represent null values.

### SDK Authentication

Authentication is handled through an API key, which can be provided in several ways:

1. Directly to the client constructor:
   ```python
   client = CBBDClient(api_key="your-api-key")
   ```

2. Through an environment variable:
   ```
   # .env file or export in shell
   CBBD_API_KEY=your-api-key
   ```

### Implemented Features

The SDK currently covers all available endpoints in the College Basketball Data API:

- Teams and rosters
- Games and schedules
- Player information and statistics
- Rankings
- Ratings
- Plays
- Betting lines
- Venues
- Conferences
- Draft data
- Recruiting information
- Lineups
- Substitutions

### Advanced Features

The SDK provides advanced features that combine multiple API calls:

1. **Team Season Profile**: Comprehensive team data for a season.
2. **Player Season Profile**: Comprehensive player data for a season.
3. **Game Analysis**: Detailed analysis of a game.

### Future Improvements

Areas identified for future work:

1. Complete test coverage
2. More examples
3. Enhanced documentation
4. CLI interface
5. More advanced features
6. PyPI package release

## GitHub Setup and Code Review (2023-03-17)

Today we performed a comprehensive code review of the project and prepared it for GitHub. Key activities included:

1. **Code Review**:
   - Assessed the overall project structure and architecture
   - Verified API wrapper implementations for completeness
   - Reviewed data transformation layer
   - Examined Streamlit demo app functionality
   - Validated model class implementations
   - Checked for branding consistency (CBBD instead of CFBD)

2. **Documentation Updates**:
   - Updated README.md to reflect current project state
   - Fixed outdated references and examples
   - Updated agentnotes.md with current status
   - Updated project_checklist.md with completed tasks and new GitHub tasks
   - Ensured documentation accurately describes the SDK functionality

3. **GitHub Preparation**:
   - Created .gitignore file for Python projects
   - Added LICENSE file (MIT)
   - Updated repository links in setup.py
   - Set author information and package metadata
   - Prepared for initial commit

4. **Next Steps**:
   - Create GitHub repository "cbbd-python-sdk"
   - Initial commit of the codebase
   - Set up branch protection rules
   - Complete remaining tasks in the project_checklist.md
   - Continue enhancing the Streamlit app with more features
   - Add comprehensive testing for all components

## 2024-03-17: Initial SDK Setup
- Created basic project structure
- Implemented core client with authentication
- Added initial API wrappers
- Created data models for API responses
- Implemented error handling and retries
- Added caching mechanism

## 2024-03-17: Streamlit App Development
- Set up Streamlit app structure
- Created pages for each API endpoint
- Added basic visualizations
- Implemented interactive controls
- Added raw data sample sections

## 2024-03-17: Transformers Implementation
- Designed transformer architecture
- Implemented base transformer class
- Created DataFrame utilities
- Added transformers for each API endpoint
- Implemented NULL value cleaning
- Built visualization-ready data converters

## 2024-03-17: Rebranding and Repository Setup
- Renamed from CFBD to CBBD throughout the codebase
- Fixed bug in Rankings page
- Fixed bug in Lines page
- Fixed bug in Plays page
- Set up GitHub repository
- Updated repository links in setup.py

## 2024-03-17: Streamlit Testing Framework
- Created comprehensive testing framework using streamlit.testing.v1.AppTest
- Implemented mock client and data fixtures for testing without hitting the real API
- Created tests for all Streamlit app pages (Teams, Games, Rankings, Ratings, Plays, Lines)
- Added tests for error handling and navigation
- Set up test runner script
- Added detailed mock data for testing all API endpoints
- Created fixtures for API responses and DataFrame transformations
- Implemented mock advanced module functionality

### Benefits of the New Testing Framework
- Can run headless tests of the Streamlit app without manual interaction
- Allows automated verification of UI components and behavior
- Can catch bugs in the app before they affect users
- Enables testing of different interaction paths
- Provides a way to test error handling
- Avoids hitting the real API during testing

### Technical Implementation Details
- Using streamlit.testing.v1.AppTest for headless testing
- pytest for test organization and execution
- unittest.mock for mocking the client and API responses
- Created fixtures directory with detailed mock data
- Implemented complete MockCBBDClient class that mimics real client behavior
- Added specific tests for each page's unique functionality

### Next Steps for Testing
- Run the tests to identify any remaining bugs in the app
- Fix issues discovered by the testing framework
- Add more edge case tests
- Integrate with CI/CD pipeline when it's set up
- Expand test coverage to include more interactions

## 2025-03-17: Added Conference Season Feature and Fixed Tests

Today we made several significant improvements to the CBBD Python SDK project:

1. **Added Conference Season Functionality**:
   - Created a new `ConferenceSeason` class in `cbbd/advanced/conference_season.py`
   - Added it to the `AdvancedAPI` class in `cbbd/advanced/__init__.py`
   - Implemented a comprehensive `get_profile` method that compiles conference data including teams, games, and standings

2. **Added Conferences Page to Streamlit App**:
   - Added "Conferences" to the navigation in the Streamlit app
   - Implemented a page that displays conference information, standings, teams, and games
   - Created a responsive UI with metrics and data tables

3. **Fixed and Extended Testing Framework**:
   - Added a test for the new Conferences page
   - Fixed issues with existing tests including the plays_page test
   - Made the testing framework more robust by ensuring all 10 tests pass consistently
   - Added conference mock data to support testing

4. **API Testing Mode**:
   - Updated the test runner to load environment variables from .env file
   - Added support for testing with either mock data or real API
   - Successfully tested with both mock data and the real API

The Conference Season feature provides a comprehensive view of a conference's performance in a given season, including standings, team records, and conference games. This feature is now fully integrated into both the SDK and the Streamlit app.

All tests are now passing, which ensures the stability of the application as we continue to add features.

## Updated Conference Season Implementation - 2024-06-13

Improved the `ConferenceSeason` class to better handle data for future seasons (2024, 2025):

1. **Enhanced Future Season Data Handling**:
   - Modified the API call strategy for future seasons to get more accurate data
   - Now retrieves all teams for future seasons first, then filters by conference
   - For games, retrieves all games and filters them by conference teams
   - Properly marks games as conference games when both teams belong to the same conference

2. **Dynamic Mock Data Usage**:
   - The app now attempts to fetch real data for ALL seasons (including 2024-2025)
   - Only falls back to mock data when real data is not available
   - Added an `is_mock_data` flag to indicate when mock data is being used
   - Updated UI to only show "mock data" warning when actual mock data is being used

These changes ensure that as real data becomes available for future seasons, the app will seamlessly start using it without requiring code changes.

## API Field Format Discoveries

- The CBBD API returns field names in camelCase, not snake_case:
  - `homeTeam` instead of `home_team`
  - `awayTeam` instead of `away_team`
  - `homePoints` instead of `home_points`
  - `awayPoints` instead of `away_points`
  - `startDate` instead of `start_date`
  - `conferenceGame` instead of `conference_game`
  - `homeConference` instead of `home_conference`
  - `awayConference` instead of `away_conference`

- The API now has a useful field `conferenceGame` that directly indicates if a game is a conference game.

## API Method Parameter Names

- Parameter names for API methods must match exactly what the underlying API expects:
  - `client.teams.get_teams(season=2023)` - Use `season` not `year`
  - `client.games.get_games(season=2023, team="Kentucky")` - Use `season` not `year`

## Object Access vs Dictionary Access

- The API client can return data in two different formats:
  1. Model Objects: Class instances with attribute access (e.g., `conf.name`, `team.school`)
  2. Dictionaries: With key access (e.g., `conf.get('name')`, `team.get('school')`)

- Our code now handles both formats by:
  - Checking if attributes exist using `hasattr()` before attempting attribute access
  - Falling back to dictionary-style access when not dealing with objects
  - Converting objects to dictionaries with `to_dict()` when available
  - Using conditional logic to determine the access pattern for each entity

## Conference Game Detection

Implemented a multi-method approach for detecting conference games:
1. First try using the `homeConference` and `awayConference` fields if available
2. Then fall back to checking if both teams are in the conference's team list
3. Finally use the `conferenceGame` field if available

## SEC Team Special Handling

For the 2024-2025 seasons, implemented special handling for SEC teams:
- Created a hardcoded list of SEC teams for these seasons
- Added fallback logic to identify conference games for these teams

## Testing

Successfully tested conference data display in multiple ways:
1. Direct API inspection test to verify field names and formats
2. Full app integration test to verify display and functionality
3. Fixed tests to use the correct camelCase field names

## Mock vs Real API Testing

- Mock API tests now pass
- Real API tests also pass using the API key from the .env file
- Tests properly load environment variables from the .env file

# CBBD Project Notebook

## API Response Structure and Insights

### Conference Data
- Conferences have `id`, `sourceId`, `name`, `abbreviation`, and `shortName` attributes
- Example SEC conference: `{'id': 24, 'sourceId': '23', 'name': 'Southeastern Conference', 'abbreviation': 'SEC', 'shortName': 'SEC'}`

### Team Data
- Teams have `name` attribute (not `school`) for the team name
- Teams have `conference` (string like "SEC") and `conference_id` (numeric like 24) attributes
- SEC conference had 14 teams in 2023 season, 16 teams in 2025 season (added Oklahoma and Texas)
- Example team data:
```
{
  'id': 264, 
  'sourceId': '2561', 
  'school': 'Siena', 
  'mascot': 'Saints', 
  'abbreviation': 'SIE', 
  'displayName': 'Siena Saints', 
  'shortDisplayName': 'Siena', 
  'primaryColor': '037961', 
  'secondaryColor': 'eea60f', 
  'currentVenueId': 71, 
  'currentVenue': 'MVP Arena', 
  'currentCity': 'Albany', 
  'currentState': 'NY', 
  'conferenceId': 16, 
  'conference': 'MAAC'
}
```

### Game Data
- Game data uses camelCase field names
- `conferenceGame` is a boolean field (not string or numeric)
- SEC 2025 season had 159 conference games and 220 non-conference games
- Complete game field list: 
```
['id', 'sourceId', 'seasonLabel', 'season', 'seasonType', 'tournament', 'startDate', 'startTimeTbd', 'neutralSite', 'conferenceGame', 'gameType', 'status', 'gameNotes', 'attendance', 'homeTeamId', 'homeTeam', 'homeConferenceId', 'homeConference', 'homeSeed', 'homePoints', 'homePeriodPoints', 'homeWinner', 'awayTeamId', 'awayTeam', 'awayConferenceId', 'awayConference', 'awaySeed', 'awayPoints', 'awayPeriodPoints', 'awayWinner', 'excitement', 'venueId', 'venue', 'city', 'state']
```

## Debugging Techniques

### Field Type Analysis
When dealing with API response fields, it's important to check:
1. Field name existence (`'conferenceGame' in games_df.columns`)
2. Field data type (`games_df['conferenceGame'].dtype`)
3. Value distribution (`games_df['conferenceGame'].value_counts()`)
4. Presence of NaN values (`games_df['conferenceGame'].isna().sum()`)
5. Actual sample values (including their Python types)

### Boolean Field Handling
For boolean fields like `conferenceGame`:
1. Direct comparison: `(games_df['conferenceGame'] == True).sum()`
2. Direct summing of boolean values: `games_df['conferenceGame'].astype(bool).sum()`
3. Using DataFrame methods: `games_df['conferenceGame'].eq(True).sum()`

### Data Verification
To ensure data correctness:
1. Cross-check related fields (e.g., conferenceGame vs. home/away conference)
2. Check for inconsistencies (games marked as conference but teams from different conferences)
3. Test at different seasons and with different conferences
4. Implement multiple methods of calculation and compare results

## Streamlit App Findings
- The app needed proper handling of boolean type for `conferenceGame` field
- Direct count using `(games_df['conferenceGame'] == True).sum()` works reliably
- Appropriate fallbacks needed when fields are missing:
  1. Try conferenceGame field first
  2. Then try homeConference/awayConference comparison
  3. Finally try team name list filtering 