"""
Exercise 1: Basic In-Memory Caching
Implement a simple in-memory cache for AI responses.

This exercise demonstrates:
1. Cache key generation with hashing
2. TTL (Time-to-Live) management
3. Cache hit/miss detection
4. Performance measurement
"""

import time
import hashlib
import json
from typing import Dict, Any, Optional

class ResponseCache:
    """
    A simple in-memory cache for AI responses.
    
    This class implements:
    - Cache key generation using SHA-256 hashing
    - TTL (Time-to-Live) management for cache expiration
    - Cache hit/miss detection
    - Basic cache statistics
    """
    
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a TTL (Time-to-Live) in seconds.
        
        Args:
            ttl (int): Time in seconds before cache entries expire (default: 60)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
        self.stats = {
            "hits": 0,
            "misses": 0,
            "total_requests": 0
        }
    
    def _make_key(self, prompt: str, params: Dict[str, Any]) -> str:
        """
        Generate a unique cache key from prompt and parameters.
        
        This method:
        1. Combines prompt and parameters into a string
        2. Uses SHA-256 hashing for consistent, fixed-length keys
        3. Ensures unique keys for different inputs
        
        Args:
            prompt (str): The AI prompt
            params (Dict[str, Any]): Model parameters (temperature, model, etc.)
            
        Returns:
            str: A unique hash key for the cache entry
        """
        # Convert parameters to a sorted string for consistency
        params_str = json.dumps(params, sort_keys=True)
        
        # Combine prompt and parameters
        raw_key = f"{prompt}_{params_str}"
        
        # Generate SHA-256 hash for consistent, fixed-length keys
        return hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
    
    def get(self, prompt: str, params: Dict[str, Any]) -> Optional[str]:
        """
        Retrieve a cached response if it exists and is not expired.
        
        This method:
        1. Generates the cache key
        2. Checks if the key exists in cache
        3. Validates TTL (Time-to-Live)
        4. Updates statistics
        5. Returns cached response or None
        
        Args:
            prompt (str): The AI prompt
            params (Dict[str, Any]): Model parameters
            
        Returns:
            Optional[str]: Cached response if valid, None if not found or expired
        """
        key = self._make_key(prompt, params)
        self.stats["total_requests"] += 1
        
        if key in self.cache:
            entry = self.cache[key]
            current_time = time.time()
            
            # Check if entry has expired based on TTL
            if current_time - entry['time'] < self.ttl:
                # Cache HIT: Entry is valid
                self.stats["hits"] += 1
                print(f"Cache HIT for key: {key[:8]}...")
                return entry['response']
            else:
                # Cache MISS: Entry has expired, remove it
                print(f"Cache EXPIRED for key: {key[:8]}...")
                del self.cache[key]
        
        # Cache MISS: Entry not found
        self.stats["misses"] += 1
        print(f"Cache MISS for key: {key[:8]}...")
        return None
    
    def set(self, prompt: str, params: Dict[str, Any], response: str) -> None:
        """
        Store a response in the cache with current timestamp.
        
        This method:
        1. Generates the cache key
        2. Stores response with current timestamp
        3. Handles cache size limits (basic implementation)
        
        Args:
            prompt (str): The AI prompt
            params (Dict[str, Any]): Model parameters
            response (str): The AI response to cache
        """
        key = self._make_key(prompt, params)
        
        # Store entry with timestamp for TTL tracking
        self.cache[key] = {
            "response": response,
            "time": time.time()
        }
        
        print(f"Cached response for key: {key[:8]}...")
        
        # Basic cache size management (optional)
        if len(self.cache) > 1000:  # Limit cache to 1000 entries
            self._cleanup_expired()
    
    def _cleanup_expired(self) -> None:
        """
        Remove expired entries from cache.
        
        This method:
        1. Iterates through all cache entries
        2. Removes entries that have exceeded TTL
        3. Helps manage memory usage
        """
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            if current_time - entry['time'] >= self.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            print(f"Cleaned up {len(expired_keys)} expired entries")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache performance statistics.
        
        Returns:
            Dict[str, Any]: Cache statistics including hit rate
        """
        total = self.stats["total_requests"]
        hits = self.stats["hits"]
        misses = self.stats["misses"]
        
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        return {
            "total_requests": total,
            "hits": hits,
            "misses": misses,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache)
        }
    
    def clear(self) -> None:
        """Clear all cached entries."""
        self.cache.clear()
        self.stats = {"hits": 0, "misses": 0, "total_requests": 0}
        print("Cache cleared")

def mock_ai_api_call(prompt: str, params: Dict[str, Any]) -> str:
    """
    Simulate an AI API call with artificial delay.
    
    This function:
    1. Simulates network delay and processing time
    2. Returns a mock response based on the prompt
    3. Demonstrates the performance benefits of caching
    
    Args:
        prompt (str): The AI prompt
        params (Dict[str, Any]): Model parameters
        
    Returns:
        str: Mock AI response
    """
    # Simulate API call delay (1-3 seconds)
    delay = 1 + (hash(prompt) % 3)  # Vary delay based on prompt
    print(f"Making API call (simulated delay: {delay}s)...")
    time.sleep(delay)
    
    # Generate mock response based on prompt
    if "capital" in prompt.lower():
        return "The capital of France is Paris."
    elif "weather" in prompt.lower():
        return "The weather is sunny with a temperature of 22°C."
    elif "math" in prompt.lower():
        return "2 + 2 = 4"
    else:
        return f"Mock response for: {prompt[:50]}..."

def demonstrate_caching():
    """
    Demonstrate the caching system with multiple test scenarios.
    
    This function shows:
    1. Cache misses for new requests
    2. Cache hits for repeated requests
    3. Performance improvements
    4. TTL expiration
    """
    print("=" * 60)
    print("EXERCISE 1: BASIC IN-MEMORY CACHING")
    print("=" * 60)
    
    # Initialize cache with 30-second TTL
    cache = ResponseCache(ttl=30)
    
    # Test parameters
    test_params = {"model": "gpt-3.5-turbo", "temperature": 0.1}
    
    print("\n1. Testing cache misses (new requests):")
    print("-" * 40)
    
    prompts = [
        "What is the capital of France?",
        "What's the weather like?",
        "What is 2 + 2?"
    ]
    
    # First round: Cache misses (slower)
    for i, prompt in enumerate(prompts, 1):
        print(f"\nRequest {i}: {prompt}")
        
        # Try to get from cache first
        cached_response = cache.get(prompt, test_params)
        
        if cached_response is None:
            # Cache miss: Make API call
            start_time = time.time()
            response = mock_ai_api_call(prompt, test_params)
            end_time = time.time()
            
            # Cache the response
            cache.set(prompt, test_params, response)
            
            print(f"Response: {response}")
            print(f"Time taken: {end_time - start_time:.2f}s (API call)")
        else:
            print(f"Response: {cached_response}")
            print("Time taken: ~0.00s (cached)")
    
    print("\n2. Testing cache hits (repeated requests):")
    print("-" * 40)
    
    # Second round: Cache hits (faster)
    for i, prompt in enumerate(prompts, 1):
        print(f"\nRequest {i}: {prompt}")
        
        start_time = time.time()
        cached_response = cache.get(prompt, test_params)
        end_time = time.time()
        
        if cached_response is None:
            # Should not happen with our TTL
            response = mock_ai_api_call(prompt, test_params)
            cache.set(prompt, test_params, response)
            print(f"Response: {response}")
            print(f"Time taken: {end_time - start_time:.2f}s (API call)")
        else:
            print(f"Response: {cached_response}")
            print(f"Time taken: {end_time - start_time:.4f}s (cached)")
    
    print("\n3. Cache Statistics:")
    print("-" * 40)
    stats = cache.get_stats()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Cache hits: {stats['hits']}")
    print(f"Cache misses: {stats['misses']}")
    print(f"Hit rate: {stats['hit_rate']:.1f}%")
    print(f"Cache size: {stats['cache_size']} entries")
    
    print("\n4. Testing TTL expiration:")
    print("-" * 40)
    print("Waiting 35 seconds for cache entries to expire...")
    time.sleep(35)  # Wait longer than TTL (30s)
    
    # Test expired cache
    prompt = "What is the capital of France?"
    print(f"\nRequest after TTL: {prompt}")
    
    cached_response = cache.get(prompt, test_params)
    if cached_response is None:
        print("Cache entry expired (expected)")
        response = mock_ai_api_call(prompt, test_params)
        cache.set(prompt, test_params, response)
    else:
        print("Cache entry still valid (unexpected)")
    
    print("\nFinal Statistics:")
    print("-" * 40)
    final_stats = cache.get_stats()
    print(f"Total requests: {final_stats['total_requests']}")
    print(f"Cache hits: {final_stats['hits']}")
    print(f"Cache misses: {final_stats['misses']}")
    print(f"Hit rate: {final_stats['hit_rate']:.1f}%")
    print(f"Cache size: {final_stats['cache_size']} entries")

def main():
    """Main function to run the caching demonstration."""
    try:
        demonstrate_caching()
        
        print("\n" + "=" * 60)
        print("EXERCISE 1 COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Key learnings:")
        print("- Cache keys are generated using SHA-256 hashing")
        print("- TTL prevents stale data from being served")
        print("- Cache hits are much faster than API calls")
        print("- Statistics help measure cache effectiveness")
        
    except Exception as e:
        print(f"Error running exercise: {e}")

if __name__ == "__main__":
    main() 