"""
Tests for the transformers module.

This module tests the data transformation functionality of the CBBD SDK.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch

from cbbd.transformers.base import BaseTransformer
from cbbd.transformers.teams import RosterTransformer, TeamsTransformer
from cbbd.transformers.utils import DataFrameUtils

class TestBaseTransformer(unittest.TestCase):
    """Tests for the BaseTransformer class."""
    
    def test_clean_null_values(self):
        """Test cleaning NULL string values."""
        # Test with NULL string
        self.assertIsNone(BaseTransformer.clean_null_values("NULL"))
        self.assertIsNone(BaseTransformer.clean_null_values("null"))
        
        # Test with non-NULL values
        self.assertEqual(BaseTransformer.clean_null_values("value"), "value")
        self.assertEqual(BaseTransformer.clean_null_values(123), 123)
        self.assertEqual(BaseTransformer.clean_null_values(None), None)
    
    def test_extract_nested_value(self):
        """Test extracting values from nested dictionaries."""
        # Test data
        data = {
            "level1": {
                "level2": {
                    "level3": "value"
                }
            },
            "empty": {},
            "null_value": "NULL"
        }
        
        # Test valid path
        self.assertEqual(
            BaseTransformer.extract_nested_value(data, "level1.level2.level3"),
            "value"
        )
        
        # Test invalid path
        self.assertIsNone(
            BaseTransformer.extract_nested_value(data, "level1.invalid.level3")
        )
        
        # Test default value
        self.assertEqual(
            BaseTransformer.extract_nested_value(data, "invalid", "default"),
            "default"
        )
        
        # Test NULL string value
        self.assertIsNone(
            BaseTransformer.extract_nested_value(data, "null_value")
        )
        
        # Test empty dict
        self.assertIsNone(
            BaseTransformer.extract_nested_value(data, "empty.key")
        )
    
    def test_flatten_dict(self):
        """Test flattening nested dictionaries."""
        # Test data
        nested = {
            "level1": {
                "level2": {
                    "level3": "value"
                },
                "level2b": "value2"
            },
            "toplevel": "top"
        }
        
        expected = {
            "level1_level2_level3": "value",
            "level1_level2b": "value2",
            "toplevel": "top"
        }
        
        flattened = BaseTransformer.flatten_dict(nested)
        self.assertEqual(flattened, expected)
        
        # Test with custom separator
        flattened_custom = BaseTransformer.flatten_dict(nested, sep=".")
        expected_custom = {
            "level1.level2.level3": "value",
            "level1.level2b": "value2",
            "toplevel": "top"
        }
        self.assertEqual(flattened_custom, expected_custom)


class TestRosterTransformer(unittest.TestCase):
    """Tests for the RosterTransformer class."""
    
    def test_to_dataframe_empty_input(self):
        """Test to_dataframe with empty input."""
        df = RosterTransformer.to_dataframe(None)
        self.assertTrue(df.empty)
        
        df = RosterTransformer.to_dataframe([])
        self.assertTrue(df.empty)
    
    def test_to_dataframe_roster_object(self):
        """Test to_dataframe with a mock roster object."""
        # Create mock roster with players
        mock_roster = MagicMock()
        
        # Create mock player
        player1 = {
            "id": 1,
            "sourceId": "123",
            "name": "Test Player",
            "firstName": "Test",
            "lastName": "Player",
            "jersey": "23",
            "position": "Guard",
            "height": 75,
            "weight": 180,
            "hometown": {
                "city": "Springfield",
                "state": "IL",
                "country": "USA",
                "latitude": 39.78,
                "longitude": -89.65,
                "countyFips": "17167"
            },
            "startSeason": 2020,
            "endSeason": 2024
        }
        
        # Player with NULL values
        player2 = {
            "id": 2,
            "sourceId": "456",
            "name": "Another Player",
            "firstName": "Another",
            "lastName": "Player",
            "jersey": "10",
            "position": "Forward",
            "height": 80,
            "weight": 220,
            "hometown": {
                "city": "NULL",
                "state": "NULL",
                "country": "NULL",
                "latitude": "NULL",
                "longitude": "NULL",
                "countyFips": "NULL"
            },
            "startSeason": "NULL",
            "endSeason": "NULL"
        }
        
        # Mock the behavior
        mock_roster._data = {
            "team": "Test Team",
            "teamId": 42,
            "conference": "Test Conference",
            "season": 2023,
            "players": [player1, player2]
        }
        
        mock_roster.get_raw_data = MagicMock(return_value=mock_roster._data)
        
        # Run the transformer
        df = RosterTransformer.to_dataframe(mock_roster)
        
        # Verify the output
        self.assertEqual(len(df), 2)
        self.assertIn('name', df.columns)
        self.assertIn('position', df.columns)
        self.assertIn('team', df.columns)
        self.assertIn('height', df.columns)
        self.assertIn('weight', df.columns)
        self.assertIn('hometown', df.columns)
        
        # Verify first player data
        self.assertEqual(df.iloc[0]['name'], "Test Player")
        self.assertEqual(df.iloc[0]['position'], "Guard")
        self.assertEqual(df.iloc[0]['team'], "Test Team")
        
        # Verify hometown string construction
        self.assertEqual(df.iloc[0]['hometown'], "Springfield, IL")
        
        # Verify conversion of NULL values
        self.assertTrue(pd.isna(df.iloc[1]['start_season']))


class TestDataFrameUtils(unittest.TestCase):
    """Tests for the DataFrameUtils class."""
    
    def test_make_visualization_ready(self):
        """Test make_visualization_ready method."""
        # Create test data
        data = {
            'numeric': ['123', '456', 'NULL', '789'],
            'categorical': ['A', 'B', 'NULL', 'C'],
            'date': ['2023-01-01', '2023-02-01', 'NULL', '2023-03-01']
        }
        df = pd.DataFrame(data)
        
        # Run the method
        result = DataFrameUtils.make_visualization_ready(
            df,
            numeric_columns=['numeric'],
            categorical_columns=['categorical'],
            date_columns=['date']
        )
        
        # Verify numeric conversion
        self.assertTrue(pd.api.types.is_numeric_dtype(result['numeric']))
        self.assertTrue(pd.isna(result.iloc[2]['numeric']))
        
        # Verify categorical conversion
        self.assertTrue(pd.api.types.is_categorical_dtype(result['categorical']))
        self.assertTrue(pd.isna(result.iloc[2]['categorical']))
        
        # Verify date conversion
        self.assertTrue(pd.api.types.is_datetime64_dtype(result['date']))
        self.assertTrue(pd.isna(result.iloc[2]['date']))
    
    def test_add_calculated_columns(self):
        """Test add_calculated_columns method."""
        # Create test data
        data = {
            'height': [72, 76, 80],
            'weight': [180, 200, 220]
        }
        df = pd.DataFrame(data)
        
        # Define calculations
        calculations = {
            'bmi': lambda df: df['weight'] / ((df['height'] / 39.37) ** 2),
            'height_in_feet': lambda df: df['height'] / 12
        }
        
        # Run the method
        result = DataFrameUtils.add_calculated_columns(df, calculations)
        
        # Verify new columns
        self.assertIn('bmi', result.columns)
        self.assertIn('height_in_feet', result.columns)
        
        # Verify values
        self.assertAlmostEqual(result.iloc[0]['height_in_feet'], 6.0)
        
    def test_standardize_column_names(self):
        """Test standardize_column_names method."""
        # Create test data with camelCase and PascalCase
        data = {
            'playerName': ['Player 1', 'Player 2'],
            'TeamId': [1, 2],
            'seasonType': ['Regular', 'Postseason']
        }
        df = pd.DataFrame(data)
        
        # Run the method
        result = DataFrameUtils.standardize_column_names(df)
        
        # Verify column names
        self.assertIn('player_name', result.columns)
        self.assertIn('team_id', result.columns)
        self.assertIn('season_type', result.columns)
        
        # Verify data preservation
        self.assertEqual(result.iloc[0]['player_name'], 'Player 1')


if __name__ == '__main__':
    unittest.main() 