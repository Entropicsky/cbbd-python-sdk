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

## Recent Changes

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

### Documentation & Testing

The documentation and testing components are partially complete:
- README.md has been updated to reflect the current state
- Example scripts have been created
- Basic tests have been implemented
- More comprehensive tests are needed for edge cases

## GitHub Setup

The next step is to create a GitHub repository for the project:

1. Create a new repository named "cbbd-python-sdk"
2. Initialize the repository with this codebase
3. Set up GitHub Actions for CI/CD (future task)
4. Create issue templates for bug reports and feature requests
5. Add a CONTRIBUTING.md file with guidelines for contributors

## Next Steps

1. **Complete Testing Suite**:
   - Add more unit tests for models and API wrappers
   - Create integration tests for the entire SDK
   - Implement automated testing for the Streamlit app

2. **Enhance Streamlit App**:
   - Add a Transformers showcase tab
   - Implement side-by-side comparisons of raw vs. transformed data
   - Create interactive code examples with copy-paste functionality
   - Add performance benchmarks visualization

3. **Package and Distribution**:
   - Finalize setup.py for PyPI distribution
   - Create proper package documentation
   - Prepare for first release

4. **Additional Features**:
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