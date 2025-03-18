# CBBD Python SDK Development Notes

## Project Structure

This project is a Python SDK for the College Basketball Data API. The project includes:

1. **Core SDK Library** (`cbbd/`): The main SDK code with API wrappers, models, and utilities
2. **Streamlit App** (`streamlit_app/`): A demo application showcasing the SDK's capabilities
3. **Examples** (`examples/`): Sample code showing how to use the SDK
4. **Tests** (`tests/`): Unit and integration tests
5. **Documentation** (`docs/`): SDK documentation

## Working Preferences

- The client prefers a methodical approach with frequent testing of each feature
- Adding debugging tools and visualization features is highly valued
- Raw API response data should be exposed to help developers understand the API
- Error handling should be thorough with detailed error messages
- Automated testing is important for maintaining quality and identifying issues

## Recent Changes

### Conference Season Feature Addition

We've implemented a new Conference Season feature that provides comprehensive data about a conference's performance in a given season:

- Created `ConferenceSeason` class in `cbbd/advanced/conference_season.py`
- Added to the `AdvancedAPI` class in `cbbd/advanced/__init__.py`
- Implemented a `get_profile` method that provides:
  - Conference information
  - Teams in the conference
  - Conference games
  - Team records (overall and conference-specific)
  - Conference standings

We also added a Conferences page to the Streamlit app that showcases this feature:
- Added to the navigation sidebar
- Displays conference information, standings, teams, and games
- Includes metrics for total games, conference games, and non-conference games
- Shows formatted standings tables with win percentages

The feature is fully tested with both mock data and real API tests.

### Streamlit Testing Framework Implementation

We've implemented a comprehensive testing framework for the Streamlit app using the `streamlit.testing.v1.AppTest` library. This allows us to:

- Run headless tests of the Streamlit app without manual interaction
- Test all UI components and interactions programmatically
- Verify data loading and visualization
- Test error handling and edge cases
- Check app navigation and functionality

The testing framework consists of:

- Mock client implementation (`MockCBBDClient`) to avoid hitting the real API
- Detailed mock data for all API endpoints
- Page-specific tests for each section of the app
- General tests for navigation and error handling
- Test runner script for easy execution

This testing framework has helped us identify and fix issues in the Streamlit app, ensuring a reliable and consistent user experience. We've also added support for testing with the real API by loading the API key from the `.env` file.

### Branding and Naming

- Changed the SDK name from CFBD (College Football Data) to CBBD (College Basketball Data)
- Updated all references in code and documentation to reflect this change
- Renamed modules, classes, and variables to use the new naming convention

### Streamlit App Improvements

- Fixed issues with the Plays page:
  - Corrected method name from `get_plays_by_game` to `get_plays`
  - Updated Play model to handle API response field names properly
  - Added proper error handling with traceback display
  
- Added "Raw Data Sample" expandable sections to all pages:
  - Teams
  - Games
  - Stats
  - Rankings
  - Ratings
  - Plays
  - Lines
  
- Fixed the Lines page to correctly process the API response

- Fixed the Roster visualization page:
  - Corrected processing of hometown data from the API
  - Added fallback visualizations when map data is unavailable
  - Improved data cleaning and NULL handling
  - Enhanced visualizations with additional context
  - Added player grouping by location and position

### Model Improvements

- Created a `BaseModel` class with standardized methods:
  - `get_raw_data()` for exposing raw API data
  - `to_dict()` for converting to dictionaries
  - `__str__()` for better string representation

## Current Status (Updated)

### Core Components

All core components have been implemented:
- Base client with authentication, error handling, and caching
- API wrappers for all endpoints (Teams, Games, Conferences, Players, etc.)
- Data models for all API responses
- Error handling with specific exception types
- Logging functionality
- Caching system to reduce API calls

### Data Transformation Layer

The data transformation layer has been implemented with:
- Base transformer classes
- DataFrame conversion utilities for all API endpoints
- Data cleaning and NULL value handling
- Nested data structure handling
- Visualization-ready data formatters
- Extension mechanisms for custom transformations

### Streamlit Demo App

The Streamlit app has been enhanced with:
- Interactive examples for all API endpoints
- Raw data sample sections for developers
- Data visualizations
- Error handling demonstrations
- Multiple pages for different API features
- Comprehensive testing framework

### Documentation & Testing

The documentation and testing components are partially complete:
- README.md has been updated to reflect the current state
- Example scripts have been created
- Basic tests have been implemented
- Streamlit app testing framework has been implemented
- More comprehensive tests are needed for edge cases

## GitHub Setup

The next step is to create a GitHub repository for the project:

1. Create a new repository named "cbbd-python-sdk"
2. Initialize the repository with this codebase
3. Set up GitHub Actions for CI/CD (future task)
4. Create issue templates for bug reports and feature requests
5. Add a CONTRIBUTING.md file with guidelines for contributors

## Next Steps

1. **Run and Verify Streamlit Tests**:
   - Execute the test framework to identify any bugs
   - Fix issues discovered by the tests
   - Expand test coverage to include more edge cases

2. **Enhance Streamlit App**:
   - Add a Transformers showcase tab
   - Implement side-by-side comparisons of raw vs. transformed data
   - Create interactive code examples with copy-paste functionality
   - Add performance benchmarks visualization

3. **Complete Testing Suite**:
   - Add more unit tests for models and API wrappers
   - Create integration tests for the entire SDK
   - Implement automated testing for the Streamlit app

4. **Package and Distribution**:
   - Finalize setup.py for PyPI distribution
   - Create proper package documentation
   - Prepare for first release

5. **Additional Features**:
   - Add pagination support for large datasets
   - Implement more advanced caching strategies
   - Create a CLI tool for quick data access

## API Key Handling

The SDK looks for API keys in the following order:
1. Directly passed to the constructor: `CBBDClient(api_key="your-key")`
2. From environment variable: `CBBD_API_KEY`
3. From environment variable: `CFBD_API_KEY` (legacy support)
4. From a .env file (loaded automatically)

For local development, the .env file should be structured as:
```
CBBD_API_KEY=your-api-key
```

## Common Issues and Solutions

- **Authentication Errors**: Usually due to invalid or expired API keys
- **Rate Limiting**: The API may impose rate limits; use caching to reduce calls
- **NULL Values in API Responses**: The transformers handle "NULL" string values automatically
- **Nested Data Structures**: Use the transformers to flatten complex data structures

## Testing Strategy

Our testing strategy includes multiple levels:

1. **Unit Testing**:
   - Core client and API wrappers
   - Data models and transformers
   - Utility functions

2. **Integration Testing**:
   - End-to-end workflows
   - Combined operations with multiple endpoints

3. **UI Testing**:
   - Streamlit app functionality
   - Component interactions
   - Data visualization

4. **Test Mocking**:
   - Mock API responses for reliable testing
   - Mock client implementation

The Streamlit app testing uses `streamlit.testing.v1.AppTest` to run headless tests that:
- Simulate user interactions
- Verify component behavior
- Check data display
- Test error handling
- Validate navigation

## Current Development

### Data Transformation Layer

We are implementing a comprehensive data transformation layer to make it easier to work with the API data. Key features:

- DataFrame conversion utilities for all API endpoints
- Standardized data cleaning and normalization
- Handling of nested data structures
- Proper NULL value processing
- Visualization-ready data formatters
- Extension mechanisms for custom transformations

This layer will address common challenges in working with the API:
1. Nested data structures that are difficult to navigate
2. String "NULL" values instead of proper null/None values
3. Inconsistent data access patterns
4. Different data formats across endpoints

The transformers will follow a consistent pattern:
```python
# Example usage
df = client.transformers.roster_to_dataframe(roster_response)
# Ready for visualization, analysis, etc.
```

## Future Work

- Implement remaining API endpoints
- Add more unit tests for edge cases
- Improve documentation with more examples
- Add TypeScript type definitions for API responses
- Create more interactive visualizations in the Streamlit app
- Consider adding a command-line interface (CLI) for quick data access 

# Agent Notes for CBBD Python SDK Project

## Project Overview

The CBBD Python SDK is a client library for accessing the College Basketball Data API. The project includes:

1. A Python SDK for accessing the API programmatically
2. A Streamlit app for interactive data exploration
3. Comprehensive testing framework

## Project Structure

```
cbbd/                # Main SDK package
│
├── client.py        # Main client class
├── endpoints/       # API endpoint modules
├── transformers/    # Data transformation utilities
├── utils/           # Helper utilities
│
streamlit_app/       # Streamlit web application
│
├── app.py           # Main Streamlit app
├── pages/           # Page implementations
│
tests/               # Test suite
├── unit/            # Unit tests for SDK
├── integration/     # Integration tests
├── streamlit/       # Streamlit app tests
│   ├── conftest.py  # Test fixtures
│   ├── test_app.py  # Streamlit tests
│   ├── test_runner.py # Test runner script
│
agent_notes/         # Agent notes and project tracking
```

## User Preferences

- The user prefers well-documented, clean code with comprehensive test coverage
- The user wants both unit tests and integration tests for all components
- The user values a modular, maintainable architecture
- The user prefers to run tests in a headless fashion
- The Streamlit app should be intuitive and well-organized

## Current Status

1. **SDK Development**: The core SDK is implemented with support for most API endpoints.
2. **Streamlit App**: A functional Streamlit app is implemented with pages for Teams, Games, Rankings, Ratings, Plays, and Lines.
3. **Testing**: Comprehensive testing framework is in place, including:
   - Unit tests for the SDK
   - Integration tests
   - Streamlit app tests using `streamlit.testing.v1.AppTest`
   - Support for both mock testing and real API testing

## Testing Framework

### Streamlit Testing

The project now includes a comprehensive testing framework for the Streamlit app using `streamlit.testing.v1.AppTest`. 

#### Running Tests

To run the tests in mock mode (no real API calls):

```bash
python3 tests/streamlit/test_runner.py -v
```

To run the tests against the real API:

```bash
python3 tests/streamlit/test_runner.py -r -v
```

The test runner automatically loads the API key from the `.env` file. The project uses the legacy API key name `CFBD_API_KEY`.

#### Test Structure

- Test fixtures are in the `tests/streamlit/fixtures` directory
- Mock client implementation is in `tests/streamlit/conftest.py`
- Test cases are in `tests/streamlit/test_app.py`
- Documentation is in `tests/streamlit/README.md`

#### Key Testing Considerations

1. **Timeouts**: Real API tests need longer timeouts, especially for data-heavy endpoints
2. **API Key**: The API key should be in the `.env` file as `CFBD_API_KEY`
3. **Test Runner Options**:
   - `-v`: Verbose output
   - `-r`: Use real API
   - `-k`: Filter tests by name pattern

## Next Steps

1. Run real API tests to identify integration issues
2. Fix bugs identified during testing
3. Enhance the Streamlit app with more visualization features
4. Implement the Advanced Analysis page
5. Add caching to improve performance
6. Prepare the SDK for publication to PyPI

## Notes for Future Sessions

- Read this file to get up to speed on the project
- Check the `agent_notes/project_checklist.md` file for current progress and tasks
- The `tests/streamlit/README.md` has detailed information about the Streamlit testing framework
- Real API testing requires the `CBBD_API_KEY` environment variable to be set 

# Agent Notes for CFBB2 Project

## Project Structure
This project is a Python client library and Streamlit application for college basketball data. It consists of:

1. A Python SDK (`cbbd` package) for interacting with the College Basketball Data API
2. A Streamlit application (`streamlit_app` folder) that provides a user interface for accessing the data

## API Data Format Insights
- The API returns data in camelCase format (e.g., `homeTeam`, `conferenceGame`, etc.)
- Team objects have a `.name` attribute (not `.school`) for the team name
- Teams have a `.conference` attribute (string) and a `.conference_id` attribute (integer)
- Games have fields like `homeTeam`, `awayTeam`, `homePoints`, `awayPoints`, `conferenceGame`
- The `conferenceGame` field is a proper boolean (True/False) data type
- When fetching teams for a conference, the preferred approach is using `get_teams(conference='SEC', season=2023)`

## Recent Fixes and Improvements
- Fixed the `ConferenceSeason` class to handle the camelCase field names from the API
- Improved team filtering to properly identify teams by conference ID or name
- Added special handling for SEC conference in 2024-2025 seasons (including Oklahoma and Texas)
- Enhanced error handling and logging throughout the codebase
- Created comprehensive test scripts for verifying API functionality
- Fixed the conference game count display in the Streamlit app to properly count boolean fields
- Implemented systematic testing and debugging to identify and fix issues

## Methodical Testing Approach
- Created dedicated test scripts to validate specific functionality (e.g., `test_conference_fields.py`, `test_game_fields.py`)
- Used detailed logging to capture data flow, field types, and value distributions
- Implemented multiple counting methods to validate and cross-check results
- Verified data integrity by comparing related fields (e.g., conferenceGame vs. homeConference/awayConference)
- Applied a first-principles approach to diagnose and fix issues

## Streamlit App
The Streamlit app has been configured to display conference data, including:
- Conference information
- Teams in the conference
- Games (both conference and non-conference)
- Standings based on conference records
- Proper counts for conference and non-conference games

## Testing Approach
- Created test scripts in `tests/api_tests/` to validate API functionality
- Used detailed logging to track API responses and data processing
- Implemented specific tests for different conferences and seasons
- Systematically tested field types and value counts

## User Preferences
- The user prefers a systematic approach with proper testing
- Documentation and clear code structure are important
- Testing should happen incrementally as features are developed
- Issues should be approached from first principles, with methodical debugging

## Next Steps
- Continue refining the Streamlit UI
- Add more comprehensive error handling
- Consider adding additional visualizations for conference data 