"""
Caching utilities for the CFBD Python SDK.
"""

import hashlib
import json
from functools import wraps
from cachetools import TTLCache

def create_cache(maxsize=128, ttl=300):
    """
    Create a TTL cache.
    
    Args:
        maxsize (int): Maximum cache size
        ttl (int): Time-to-live in seconds
        
    Returns:
        TTLCache: Cache instance
    """
    return TTLCache(maxsize=maxsize, ttl=ttl)

def generate_cache_key(func_name, args, kwargs):
    """
    Generate a cache key from function name and arguments.
    
    Args:
        func_name (str): Function name
        args (tuple): Positional arguments
        kwargs (dict): Keyword arguments
        
    Returns:
        str: Cache key
    """
    # Convert args and kwargs to a string representation
    key_parts = [func_name]
    
    if args:
        key_parts.append(str(args))
    
    if kwargs:
        # Sort kwargs by key for consistent ordering
        sorted_kwargs = sorted(kwargs.items())
        key_parts.append(str(sorted_kwargs))
    
    # Join parts and create a hash
    key_str = "_".join(key_parts)
    return hashlib.md5(key_str.encode()).hexdigest()

def cached(func):
    """
    Decorator for caching API responses.
    
    Args:
        func: Function to cache
        
    Returns:
        Function wrapper with caching
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Skip caching if disabled
        if not self.client.use_cache:
            return func(self, *args, **kwargs)
        
        # Generate cache key
        cache_key = generate_cache_key(func.__name__, args, kwargs)
        
        # Check cache
        if cache_key in self.client.cache:
            return self.client.cache[cache_key]
        
        # Make request and cache result
        result = func(self, *args, **kwargs)
        self.client.cache[cache_key] = result
        return result
    
    return wrapper 