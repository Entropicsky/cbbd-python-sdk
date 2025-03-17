"""
Tests for the cache utilities.
"""

import pytest
import time
from unittest.mock import MagicMock, call

from cbbd.utils.cache import (
    create_cache,
    generate_cache_key,
    cached
)


class TestCache:
    """Tests for the cache utilities."""
    
    def test_create_cache(self):
        """Test create_cache function."""
        # Test with default parameters
        cache = create_cache()
        assert cache.maxsize == 128
        assert cache.ttl == 300
        
        # Test with custom parameters
        cache = create_cache(maxsize=256, ttl=600)
        assert cache.maxsize == 256
        assert cache.ttl == 600
    
    def test_generate_cache_key(self):
        """Test generate_cache_key function."""
        # Test with function name only
        key1 = generate_cache_key("test_func", (), {})
        assert isinstance(key1, str)
        
        # Test with positional arguments
        key2 = generate_cache_key("test_func", (1, "two", 3.0), {})
        assert isinstance(key2, str)
        assert key1 != key2
        
        # Test with keyword arguments
        key3 = generate_cache_key("test_func", (), {"a": 1, "b": "two"})
        assert isinstance(key3, str)
        assert key1 != key3
        
        # Test with positional and keyword arguments
        key4 = generate_cache_key("test_func", (1, "two"), {"a": 1, "b": "two"})
        assert isinstance(key4, str)
        assert key1 != key4
        
        # Test same arguments produce same key
        key5 = generate_cache_key("test_func", (1, "two"), {"a": 1, "b": "two"})
        assert key4 == key5
        
        # Test different order of keyword arguments produce same key
        key6 = generate_cache_key("test_func", (1, "two"), {"b": "two", "a": 1})
        assert key4 == key6
    
    def test_cached_decorator(self):
        """Test cached decorator."""
        # Create a mock class similar to API classes
        class TestAPI:
            def __init__(self):
                self.client = MagicMock()
                self.client.use_cache = True
                self.client.cache = {}
                self.counter = 0
            
            @cached
            def test_method(self, arg1, arg2=None):
                self.counter += 1
                return f"{arg1}-{arg2}"
        
        # Test caching is working
        api = TestAPI()
        
        # First call should not be cached
        result1 = api.test_method("value1", arg2="value2")
        assert result1 == "value1-value2"
        assert api.counter == 1
        assert len(api.client.cache) == 1
        
        # Second call with same arguments should be cached
        result2 = api.test_method("value1", arg2="value2")
        assert result2 == "value1-value2"
        assert api.counter == 1  # Counter should not increase
        
        # Call with different arguments should not be cached
        result3 = api.test_method("value3", arg2="value4")
        assert result3 == "value3-value4"
        assert api.counter == 2
        assert len(api.client.cache) == 2
    
    def test_cached_decorator_with_cache_disabled(self):
        """Test cached decorator with cache disabled."""
        # Create a mock class with cache disabled
        class TestAPI:
            def __init__(self):
                self.client = MagicMock()
                self.client.use_cache = False
                self.counter = 0
            
            @cached
            def test_method(self, arg1, arg2=None):
                self.counter += 1
                return f"{arg1}-{arg2}"
        
        # Test that cache is bypassed
        api = TestAPI()
        
        # Calls should always execute the method
        api.test_method("value1", arg2="value2")
        assert api.counter == 1
        
        api.test_method("value1", arg2="value2")
        assert api.counter == 2
    
    def test_cached_decorator_with_ttl(self):
        """Test cached decorator with TTL."""
        # Create a mock class with a short TTL cache
        class TestAPI:
            def __init__(self):
                self.client = MagicMock()
                self.client.use_cache = True
                self.client.cache = create_cache(ttl=0.1)  # 100ms TTL for testing
                self.counter = 0
            
            @cached
            def test_method(self, arg1):
                self.counter += 1
                return arg1
        
        # Test that cache expires after TTL
        api = TestAPI()
        
        api.test_method("value")
        assert api.counter == 1
        
        # This should be cached
        api.test_method("value")
        assert api.counter == 1
        
        # Wait for cache to expire
        time.sleep(0.2)
        
        # This should execute the method again
        api.test_method("value")
        assert api.counter == 2 