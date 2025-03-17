# CFBD Python SDK Testing Plan

## Testing Strategy Overview

This document outlines the testing strategy for the CFBD Python SDK, which will ensure the quality, reliability, and performance of the SDK.

## Testing Levels

### 1. Unit Testing

Unit tests will verify the functionality of individual components in isolation.

#### Core Components to Test
- Client initialization and configuration
- Model class instantiation and properties
- API endpoint wrapper methods
- Utility functions
- Error handling
- Caching mechanism

#### Unit Test Examples

```python
# Test client initialization
def test_client_init_with_api_key():
    client = CFBDClient(api_key="test_key")
    assert client.api_key == "test_key"

def test_client_init_without_api_key_raises_error():
    with pytest.raises(ValueError):
        # Assuming no CFBD_API_KEY in environment
        CFBDClient()

# Test model properties
def test_team_model_properties():
    data = {
        "id": 123,
        "school": "Test University",
        "mascot": "Testers",
        "conference": "Test Conference"
    }
    team = Team(data)
    assert team.id == 123
    assert team.name == "Test University"
    assert team.mascot == "Testers"
    assert team.conference == "Test Conference"

# Test API request handling
def test_api_request_with_mock(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"test": "data"}
    mock_response.status_code = 200
    
    mocker.patch("requests.get", return_value=mock_response)
    
    client = CFBDClient(api_key="test_key")
    base_api = BaseAPI(client)
    result = base_api._request("/test", {"param": "value"})
    
    assert result == {"test": "data"}
    requests.get.assert_called_once()
```

### 2. Integration Testing

Integration tests will verify that different components work together correctly.

#### Key Integration Points to Test
- Client with API endpoints
- API endpoints with models
- Advanced functionality combining multiple API calls
- Error propagation across components

#### Integration Test Examples

```python
# Test API endpoint with client (mock response)
def test_get_teams_integration(mocker):
    mock_data = [
        {"id": 1, "school": "Team A", "mascot": "Lions"},
        {"id": 2, "school": "Team B", "mascot": "Tigers"}
    ]
    mock_response = mocker.Mock()
    mock_response.json.return_value = mock_data
    mock_response.status_code = 200
    
    mocker.patch("requests.get", return_value=mock_response)
    
    client = CFBDClient(api_key="test_key")
    teams = client.teams.get_teams()
    
    assert len(teams) == 2
    assert teams[0].name == "Team A"
    assert teams[1].name == "Team B"

# Test advanced functionality
def test_team_season_profile_integration(mocker):
    # Mock multiple API calls
    mock_team_data = {"id": 1, "school": "Test University"}
    mock_games_data = [{"id": 101, "homeTeam": "Test University"}]
    mock_stats_data = [{"teamId": 1, "points": 75}]
    
    def mock_request(endpoint, params=None):
        if endpoint == "/teams":
            return [mock_team_data]
        elif endpoint == "/games":
            return mock_games_data
        elif endpoint == "/stats/team/season":
            return mock_stats_data
        return []
    
    mocker.patch.object(BaseAPI, "_request", side_effect=mock_request)
    
    client = CFBDClient(api_key="test_key")
    profile = client.team_seasons.get_profile("Test University", 2023)
    
    assert profile["team"]["name"] == "Test University"
    assert len(profile["games"]) == 1
    assert profile["stats"]["points"] == 75
```

### 3. End-to-End Testing

End-to-end tests will verify the SDK works correctly against the actual API.

#### Key End-to-End Scenarios
- Basic API calls with real API key
- Error handling with invalid requests
- Rate limiting handling
- Caching behavior with multiple calls

#### End-to-End Test Examples

```python
# Note: These tests require a real API key and access to the API
# They should be skipped if no API key is available

@pytest.mark.skipif(os.getenv("CFBD_API_KEY") is None, reason="No API key available")
def test_get_teams_e2e():
    client = CFBDClient()
    teams = client.teams.get_teams()
    assert len(teams) > 0
    assert isinstance(teams[0], Team)

@pytest.mark.skipif(os.getenv("CFBD_API_KEY") is None, reason="No API key available")
def test_get_games_with_filter_e2e():
    client = CFBDClient()
    games = client.games.get_games(team="Duke", season=2023)
    assert len(games) > 0
    assert all(g.season == 2023 for g in games)
    assert any(g.home_team == "Duke" or g.away_team == "Duke" for g in games)
```

### 4. Performance Testing

Performance tests will verify the SDK meets performance requirements.

#### Key Performance Metrics
- Response time for API calls
- Cache hit/miss performance
- Memory usage with large response sets

#### Performance Test Examples

```python
def test_caching_performance():
    client = CFBDClient(api_key="test_key", use_cache=True)
    
    # First call - should hit API
    start_time = time.time()
    teams1 = client.teams.get_teams()
    first_call_time = time.time() - start_time
    
    # Second call - should hit cache
    start_time = time.time()
    teams2 = client.teams.get_teams()
    second_call_time = time.time() - start_time
    
    assert second_call_time < first_call_time
    assert teams1 == teams2
```

## Mock Responses

We'll create a collection of mock responses for testing without requiring API access:

```python
# teams.py
MOCK_TEAMS_RESPONSE = [
    {
        "id": 1,
        "sourceId": "123",
        "school": "Test University",
        "mascot": "Testers",
        "abbreviation": "TEST",
        "displayName": "Test University Testers",
        "shortDisplayName": "Test",
        "primaryColor": "FF0000",
        "secondaryColor": "0000FF",
        "currentVenueId": 1,
        "currentVenue": "Test Arena",
        "currentCity": "Testville",
        "currentState": "TS",
        "conferenceId": 1,
        "conference": "Test Conference"
    },
    # More teams...
]

# games.py
MOCK_GAMES_RESPONSE = [
    {
        "id": 101,
        "sourceId": "456",
        "seasonLabel": "20222023",
        "season": 2023,
        "seasonType": "regular",
        "startDate": "2022-11-07T19:00:00.000Z",
        "homeTeamId": 1,
        "homeTeam": "Test University",
        "homeConferenceId": 1,
        "homeConference": "Test Conference",
        "homePoints": 80,
        "awayTeamId": 2,
        "awayTeam": "Rival University",
        "awayConferenceId": 2,
        "awayConference": "Rival Conference",
        "awayPoints": 70
    },
    # More games...
]

# Additional mock responses for other endpoints...
```

## Test Fixtures

We'll use pytest fixtures to set up common test environments:

```python
@pytest.fixture
def mock_client(mocker):
    """Create a client with mocked HTTP session."""
    client = CFBDClient(api_key="test_key")
    mock_session = mocker.Mock()
    client._session = mock_session
    return client, mock_session

@pytest.fixture
def mock_teams_response():
    """Return mock teams response data."""
    return copy.deepcopy(MOCK_TEAMS_RESPONSE)

@pytest.fixture
def mock_games_response():
    """Return mock games response data."""
    return copy.deepcopy(MOCK_GAMES_RESPONSE)
```

## Test Directory Structure

```
tests/
├── conftest.py              # Common fixtures
├── mock_responses/          # Mock API responses
│   ├── __init__.py
│   ├── teams.py
│   ├── games.py
│   └── ...
├── unit/                    # Unit tests
│   ├── test_client.py
│   ├── test_base_api.py
│   ├── test_teams_api.py
│   ├── test_models.py
│   └── ...
├── integration/             # Integration tests
│   ├── test_client_api.py
│   ├── test_advanced.py
│   └── ...
└── e2e/                     # End-to-end tests
    ├── test_api_calls.py
    └── ...
```

## Test Execution

### Prerequisites
- pytest
- pytest-mock
- pytest-cov (for coverage reporting)

### Running Tests
- Unit tests: `pytest tests/unit/`
- Integration tests: `pytest tests/integration/`
- End-to-end tests: `pytest tests/e2e/`
- All tests: `pytest`
- With coverage: `pytest --cov=cfbd`

### CI/CD Integration
Tests will be integrated into the CI/CD pipeline:
- Run unit and integration tests on every push
- Run end-to-end tests on pull requests and releases
- Generate coverage reports
- Fail builds if coverage drops below threshold

## Test-Driven Development Approach

We'll use TDD for developing the SDK:
1. Write tests for the desired behavior
2. Implement the code to make the tests pass
3. Refactor as needed
4. Repeat for each feature

This approach ensures we maintain high test coverage and that the code meets requirements.

## Testing Edge Cases

We'll specifically test edge cases such as:
- Empty responses
- Large response sets
- API errors
- Network failures
- Invalid input parameters
- Rate limiting responses
- Authentication failures

## Test Documentation

Each test module will include docstrings explaining:
- What is being tested
- Test dependencies
- Expected behavior
- Edge cases covered

## Test Maintenance

Tests will be maintained alongside code changes:
- Update tests when API changes
- Add tests for new features
- Refactor tests to improve clarity and maintainability 