"""
Exercise 2: Persistent Disk Caching
Implement disk-based caching for persistence across application restarts.

This exercise demonstrates:
1. Persistent storage using diskcache library
2. Cross-session data retention
3. Disk I/O optimization
4. Cache persistence management
"""

import time
import hashlib
import json
import os
from typing import Dict, Any, Optional
from diskcache import Cache

class PersistentResponseCache:
    """
    A persistent disk-based cache for AI responses.
    
    This class implements:
    - Persistent storage using diskcache library
    - TTL (Time-to-Live) management for cache expiration
    - Cross-session data retention
    - Disk I/O optimization with compression
    """
    
    def __init__(self, cache_dir: str = "./cache", ttl: int = 3600):
        """
        Initialize the persistent cache with disk storage.
        
        Args:
            cache_dir (str): Directory to store cache files (default: "./cache")
            ttl (int): Time in seconds before cache entries expire (default: 3600 = 1 hour)
        """
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize diskcache with compression and other optimizations
        self.cache = Cache(
            directory=cache_dir,
            size_limit=100 * 1024 * 1024,  # 100MB limit
            compression_level=6,  # Good compression ratio
            disk_min_file_size=1024,  # Compress files > 1KB
            disk_pickle_protocol=4  # Use newer pickle protocol
        )
        
        self.ttl = ttl
        self.stats = {
            "hits": 0,
            "misses": 0,
            "total_requests": 0,
            "disk_size": 0
        }
        
        print(f"Persistent cache initialized in: {cache_dir}")
        print(f"Cache TTL: {ttl} seconds ({ttl/3600:.1f} hours)")
    
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
        2. Checks if the key exists in disk cache
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
        
        try:
            # Try to get from disk cache
            cached_data = self.cache.get(key)
            
            if cached_data is not None:
                # Unpack cached data
                response, timestamp = cached_data
                current_time = time.time()
                
                # Check if entry has expired based on TTL
                if current_time - timestamp < self.ttl:
                    # Cache HIT: Entry is valid
                    self.stats["hits"] += 1
                    print(f"Disk Cache HIT for key: {key[:8]}...")
                    return response
                else:
                    # Cache EXPIRED: Entry has expired, remove it
                    print(f"Disk Cache EXPIRED for key: {key[:8]}...")
                    self.cache.delete(key)
            
            # Cache MISS: Entry not found
            self.stats["misses"] += 1
            print(f"Disk Cache MISS for key: {key[:8]}...")
            return None
            
        except Exception as e:
            print(f"Error reading from disk cache: {e}")
            self.stats["misses"] += 1
            return None
    
    def set(self, prompt: str, params: Dict[str, Any], response: str) -> None:
        """
        Store a response in the disk cache with current timestamp.
        
        This method:
        1. Generates the cache key
        2. Stores response with current timestamp on disk
        3. Uses compression to save disk space
        4. Handles disk I/O errors gracefully
        
        Args:
            prompt (str): The AI prompt
            params (Dict[str, Any]): Model parameters
            response (str): The AI response to cache
        """
        key = self._make_key(prompt, params)
        
        try:
            # Store entry with timestamp for TTL tracking
            # Use tuple to store both response and timestamp
            cached_data = (response, time.time())
            
            # Store in disk cache (automatically compressed)
            self.cache.set(key, cached_data)
            
            print(f"Disk cached response for key: {key[:8]}...")
            
        except Exception as e:
            print(f"Error writing to disk cache: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache performance statistics including disk usage.
        
        Returns:
            Dict[str, Any]: Cache statistics including hit rate and disk usage
        """
        total = self.stats["total_requests"]
        hits = self.stats["hits"]
        misses = self.stats["misses"]
        
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        # Get disk cache statistics
        try:
            disk_size = self.cache.volume()
            cache_size = len(self.cache)
        except Exception as e:
            disk_size = 0
            cache_size = 0
            print(f"Error getting disk cache stats: {e}")
        
        return {
            "total_requests": total,
            "hits": hits,
            "misses": misses,
            "hit_rate": hit_rate,
            "cache_size": cache_size,
            "disk_size_mb": disk_size / (1024 * 1024) if disk_size else 0
        }
    
    def clear(self) -> None:
        """Clear all cached entries from disk."""
        try:
            self.cache.clear()
            self.stats = {"hits": 0, "misses": 0, "total_requests": 0, "disk_size": 0}
            print("Disk cache cleared")
        except Exception as e:
            print(f"Error clearing disk cache: {e}")
    
    def cleanup_expired(self) -> int:
        """
        Remove expired entries from disk cache.
        
        Returns:
            int: Number of expired entries removed
        """
        current_time = time.time()
        expired_count = 0
        
        try:
            # Iterate through all cache keys
            for key in self.cache.iterkeys():
                cached_data = self.cache.get(key)
                if cached_data is not None:
                    response, timestamp = cached_data
                    if current_time - timestamp >= self.ttl:
                        self.cache.delete(key)
                        expired_count += 1
            
            if expired_count > 0:
                print(f"Cleaned up {expired_count} expired entries from disk")
            
        except Exception as e:
            print(f"Error cleaning up expired entries: {e}")
        
        return expired_count

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
    elif "history" in prompt.lower():
        return "The French Revolution began in 1789."
    else:
        return f"Mock response for: {prompt[:50]}..."

def demonstrate_persistent_caching():
    """
    Demonstrate the persistent caching system with multiple test scenarios.
    
    This function shows:
    1. Cache persistence across sessions
    2. Disk storage benefits
    3. Performance improvements
    4. TTL expiration with disk storage
    """
    print("=" * 60)
    print("EXERCISE 2: PERSISTENT DISK CACHING")
    print("=" * 60)
    
    # Initialize persistent cache with 1-hour TTL
    cache = PersistentResponseCache(ttl=3600)  # 1 hour TTL
    
    # Test parameters
    test_params = {"model": "gpt-3.5-turbo", "temperature": 0.1}
    
    print("\n1. Testing persistent cache (new requests):")
    print("-" * 40)
    
    prompts = [
        "What is the capital of France?",
        "What's the weather like?",
        "What is 2 + 2?",
        "Tell me about French history."
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
            
            # Cache the response on disk
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
    print(f"Disk usage: {stats['disk_size_mb']:.2f} MB")
    
    print("\n4. Testing persistence (simulating restart):")
    print("-" * 40)
    print("Simulating application restart...")
    print("(In a real scenario, the application would restart here)")
    print("Creating new cache instance with same directory...")
    
    # Simulate restart by creating new cache instance
    new_cache = PersistentResponseCache(ttl=3600)
    
    # Test if data persists
    test_prompt = "What is the capital of France?"
    print(f"\nTesting persistence with: {test_prompt}")
    
    cached_response = new_cache.get(test_prompt, test_params)
    if cached_response is not None:
        print("SUCCESS: Cache data persisted across restart!")
        print(f"Retrieved: {cached_response}")
    else:
        print("Cache miss (expected if TTL expired or first run)")
    
    print("\n5. Testing cache cleanup:")
    print("-" * 40)
    expired_count = new_cache.cleanup_expired()
    print(f"Expired entries removed: {expired_count}")
    
    print("\nFinal Statistics:")
    print("-" * 40)
    final_stats = new_cache.get_stats()
    print(f"Total requests: {final_stats['total_requests']}")
    print(f"Cache hits: {final_stats['hits']}")
    print(f"Cache misses: {final_stats['misses']}")
    print(f"Hit rate: {final_stats['hit_rate']:.1f}%")
    print(f"Cache size: {final_stats['cache_size']} entries")
    print(f"Disk usage: {final_stats['disk_size_mb']:.2f} MB")

def main():
    """Main function to run the persistent caching demonstration."""
    try:
        demonstrate_persistent_caching()
        
        print("\n" + "=" * 60)
        print("EXERCISE 2 COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Key learnings:")
        print("- Disk cache persists data across application restarts")
        print("- Compression reduces disk space usage")
        print("- TTL works with persistent storage")
        print("- Disk I/O is slower than memory but provides persistence")
        print("- Cache directory can be shared across multiple instances")
        
    except Exception as e:
        print(f"Error running exercise: {e}")
        print("Make sure you have diskcache installed: pip install diskcache")

if __name__ == "__main__":
    main() 