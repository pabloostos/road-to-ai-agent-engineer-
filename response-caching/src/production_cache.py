"""
Exercise 4: Production-Ready Caching System
Implement a production-ready caching system with advanced features.

This exercise demonstrates:
1. Advanced error handling and recovery
2. Cache invalidation strategies
3. Memory management and optimization
4. Safety mechanisms and monitoring
5. Distributed cache considerations
"""

import time
import hashlib
import json
import threading
import logging
from typing import Dict, Any, Optional, List
from collections import OrderedDict
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CacheEvictionPolicy(Enum):
    """Cache eviction policies."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    FIFO = "fifo"  # First In, First Out

class ProductionCache:
    """
    A production-ready caching system with advanced features.
    
    Features:
    - Multiple eviction policies
    - Memory management
    - Thread safety
    - Error handling and recovery
    - Cache invalidation strategies
    - Performance monitoring
    """
    
    def __init__(self, 
                 max_size: int = 1000,
                 ttl: int = 3600,
                 eviction_policy: CacheEvictionPolicy = CacheEvictionPolicy.LRU):
        """
        Initialize the production cache.
        
        Args:
            max_size (int): Maximum number of cache entries
            ttl (int): Default time-to-live in seconds
            eviction_policy (CacheEvictionPolicy): Cache eviction strategy
        """
        self.max_size = max_size
        self.default_ttl = ttl
        self.eviction_policy = eviction_policy
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Cache storage
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        
        # Statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "errors": 0,
            "total_requests": 0,
            "start_time": time.time()
        }
        
        logger.info(f"Production cache initialized: max_size={max_size}, "
                   f"policy={eviction_policy.value}")
    
    def _make_key(self, prompt: str, params: Dict[str, Any]) -> str:
        """Generate a cache key."""
        params_str = json.dumps(params, sort_keys=True)
        raw_key = f"{prompt}_{params_str}"
        return hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
    
    def _cleanup_expired(self):
        """Remove expired entries from cache."""
        with self._lock:
            expired_keys = []
            current_time = time.time()
            
            for key, entry in self._cache.items():
                if current_time - entry['created_at'] > entry['ttl']:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
                logger.debug(f"Removed expired entry: {key[:8]}...")
    
    def _enforce_size_limits(self):
        """Enforce cache size limits using eviction policy."""
        with self._lock:
            while len(self._cache) > self.max_size:
                if len(self._cache) == 0:
                    break
                
                # Choose entry to evict based on policy
                key_to_evict = self._select_eviction_candidate()
                if key_to_evict:
                    del self._cache[key_to_evict]
                    self.stats["evictions"] += 1
                    logger.debug(f"Evicted entry: {key_to_evict[:8]}...")
    
    def _select_eviction_candidate(self) -> Optional[str]:
        """Select an entry to evict based on the eviction policy."""
        if not self._cache:
            return None
        
        if self.eviction_policy == CacheEvictionPolicy.LRU:
            # Remove least recently used (first in OrderedDict)
            return next(iter(self._cache))
        
        elif self.eviction_policy == CacheEvictionPolicy.LFU:
            # Remove least frequently used
            min_access_count = float('inf')
            candidate = None
            for key, entry in self._cache.items():
                if entry['access_count'] < min_access_count:
                    min_access_count = entry['access_count']
                    candidate = key
            return candidate
        
        elif self.eviction_policy == CacheEvictionPolicy.FIFO:
            # Remove first in (same as LRU for OrderedDict)
            return next(iter(self._cache))
        
        return next(iter(self._cache))  # Default to first
    
    def get(self, prompt: str, params: Dict[str, Any]) -> Optional[str]:
        """
        Get a cached response with comprehensive error handling.
        
        Args:
            prompt (str): The AI prompt
            params (Dict[str, Any]): Model parameters
            
        Returns:
            Optional[str]: Cached response or None if not found
        """
        key = self._make_key(prompt, params)
        self.stats["total_requests"] += 1
        
        try:
            with self._lock:
                # Cleanup expired entries first
                self._cleanup_expired()
                
                if key in self._cache:
                    entry = self._cache[key]
                    current_time = time.time()
                    
                    # Check if entry is still valid
                    if current_time - entry['created_at'] <= entry['ttl']:
                        # Cache HIT
                        entry['access_count'] += 1
                        entry['last_accessed'] = current_time
                        self._cache.move_to_end(key)  # Move to end for LRU
                        self.stats["hits"] += 1
                        
                        logger.debug(f"Cache HIT: {key[:8]}...")
                        return entry['value']
                    else:
                        # Entry has expired
                        del self._cache[key]
                
                # Cache MISS
                self.stats["misses"] += 1
                logger.debug(f"Cache MISS: {key[:8]}...")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving from cache: {e}")
            self.stats["errors"] += 1
            return None
    
    def set(self, prompt: str, params: Dict[str, Any], response: str, 
            ttl: Optional[int] = None) -> bool:
        """
        Set a cached response with error handling.
        
        Args:
            prompt (str): The AI prompt
            params (Dict[str, Any]): Model parameters
            response (str): The AI response
            ttl (Optional[int]): Custom TTL for this entry
            
        Returns:
            bool: True if successfully cached, False otherwise
        """
        key = self._make_key(prompt, params)
        
        try:
            with self._lock:
                # Check if we need to evict entries
                if len(self._cache) >= self.max_size:
                    self._enforce_size_limits()
                
                # Add new entry
                current_time = time.time()
                self._cache[key] = {
                    'value': response,
                    'created_at': current_time,
                    'last_accessed': current_time,
                    'access_count': 1,
                    'ttl': ttl or self.default_ttl
                }
                
                logger.debug(f"Cached response: {key[:8]}...")
                return True
                
        except Exception as e:
            logger.error(f"Error setting cache entry: {e}")
            self.stats["errors"] += 1
            return False
    
    def invalidate(self, prompt: str, params: Dict[str, Any]) -> bool:
        """
        Invalidate a specific cache entry.
        
        Args:
            prompt (str): The AI prompt
            params (Dict[str, Any]): Model parameters
            
        Returns:
            bool: True if entry was invalidated, False if not found
        """
        key = self._make_key(prompt, params)
        
        try:
            with self._lock:
                if key in self._cache:
                    del self._cache[key]
                    logger.info(f"Invalidated cache entry: {key[:8]}...")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Error invalidating cache entry: {e}")
            self.stats["errors"] += 1
            return False
    
    def clear(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            int: Number of entries cleared
        """
        try:
            with self._lock:
                count = len(self._cache)
                self._cache.clear()
                logger.info(f"Cleared {count} cache entries")
                return count
                
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            self.stats["errors"] += 1
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        with self._lock:
            total = self.stats["total_requests"]
            hits = self.stats["hits"]
            misses = self.stats["misses"]
            
            hit_rate = (hits / total * 100) if total > 0 else 0
            
            return {
                "basic_stats": {
                    "total_requests": total,
                    "hits": hits,
                    "misses": misses,
                    "hit_rate": hit_rate,
                    "evictions": self.stats["evictions"],
                    "errors": self.stats["errors"]
                },
                "cache_stats": {
                    "current_entries": len(self._cache),
                    "max_entries": self.max_size,
                    "usage_percent": (len(self._cache) / self.max_size) * 100
                },
                "configuration": {
                    "eviction_policy": self.eviction_policy.value,
                    "default_ttl": self.default_ttl
                },
                "uptime": time.time() - self.stats["start_time"]
            }

def mock_ai_api_call(prompt: str, params: Dict[str, Any]) -> str:
    """Simulate an AI API call with artificial delay."""
    delay = 1 + (hash(prompt) % 3)
    print(f"Making API call (simulated delay: {delay}s)...")
    time.sleep(delay)
    
    if "capital" in prompt.lower():
        return "The capital of France is Paris."
    elif "weather" in prompt.lower():
        return "The weather is sunny with a temperature of 22°C."
    elif "math" in prompt.lower():
        return "2 + 2 = 4"
    else:
        return f"Mock response for: {prompt[:50]}..."

def demonstrate_production_cache():
    """
    Demonstrate the production-ready caching system.
    """
    print("=" * 60)
    print("EXERCISE 4: PRODUCTION-READY CACHING SYSTEM")
    print("=" * 60)
    
    # Initialize production cache with different configurations
    cache_configs = [
        {
            "name": "LRU Cache (Small)",
            "max_size": 5,
            "eviction_policy": CacheEvictionPolicy.LRU
        },
        {
            "name": "LFU Cache (Medium)",
            "max_size": 10,
            "eviction_policy": CacheEvictionPolicy.LFU
        },
        {
            "name": "FIFO Cache (Large)",
            "max_size": 15,
            "eviction_policy": CacheEvictionPolicy.FIFO
        }
    ]
    
    test_params = {"model": "gpt-3.5-turbo", "temperature": 0.1}
    
    for config in cache_configs:
        print(f"\n1. Testing {config['name']}:")
        print("-" * 40)
        
        # Create cache instance
        cache = ProductionCache(
            max_size=config["max_size"],
            eviction_policy=config["eviction_policy"],
            ttl=30
        )
        
        # Test prompts
        prompts = [
            "What is the capital of France?",
            "What's the weather like?",
            "What is 2 + 2?",
            "Tell me about AI",
            "Explain machine learning",
            "What is the capital of France?",  # Repeat
            "What's the weather like?",        # Repeat
            "New prompt 1",
            "New prompt 2",
            "New prompt 3",
            "New prompt 4",
            "New prompt 5",
            "New prompt 6",
            "New prompt 7",
            "New prompt 8"
        ]
        
        # Process requests
        for i, prompt in enumerate(prompts, 1):
            print(f"\nRequest {i}: {prompt}")
            
            cached_response = cache.get(prompt, test_params)
            
            if cached_response is None:
                # Cache miss: Make API call
                response = mock_ai_api_call(prompt, test_params)
                success = cache.set(prompt, test_params, response)
                
                if success:
                    print(f"Response: {response}")
                    print("Status: Cached successfully")
                else:
                    print("Status: Failed to cache")
            else:
                print(f"Response: {cached_response}")
                print("Status: Retrieved from cache")
        
        # Display statistics
        print(f"\n2. {config['name']} Statistics:")
        print("-" * 40)
        
        stats = cache.get_stats()
        
        basic = stats["basic_stats"]
        cache_stats = stats["cache_stats"]
        config_info = stats["configuration"]
        
        print(f"Total requests: {basic['total_requests']}")
        print(f"Cache hits: {basic['hits']}")
        print(f"Cache misses: {basic['misses']}")
        print(f"Hit rate: {basic['hit_rate']:.1f}%")
        print(f"Evictions: {basic['evictions']}")
        print(f"Errors: {basic['errors']}")
        
        print(f"\nCache Usage:")
        print(f"Current entries: {cache_stats['current_entries']}/{cache_stats['max_entries']}")
        print(f"Usage: {cache_stats['usage_percent']:.1f}%")
        
        print(f"\nConfiguration:")
        print(f"Eviction policy: {config_info['eviction_policy']}")
        print(f"Default TTL: {config_info['default_ttl']}s")
        
        print(f"\nUptime: {stats['uptime']:.1f}s")
        
        # Test cache invalidation
        print(f"\n3. Testing Cache Invalidation:")
        print("-" * 40)
        
        test_prompt = "What is the capital of France?"
        print(f"Invalidating: {test_prompt}")
        
        if cache.invalidate(test_prompt, test_params):
            print("Entry invalidated successfully")
            
            # Try to get the invalidated entry
            cached_response = cache.get(test_prompt, test_params)
            if cached_response is None:
                print("Entry no longer available (expected)")
            else:
                print("Entry still available (unexpected)")
        else:
            print("Entry not found for invalidation")
        
        # Clear cache
        cleared_count = cache.clear()
        print(f"\nCleared {cleared_count} cache entries")
        
        print(f"\n{config['name']} test completed.")
        print("=" * 60)
    
    print("\n4. Production Features Demonstrated:")
    print("-" * 40)
    print("✓ Thread-safe operations with RLock")
    print("✓ Multiple eviction policies (LRU, LFU, FIFO)")
    print("✓ Memory management and size limits")
    print("✓ Comprehensive error handling")
    print("✓ Cache invalidation strategies")
    print("✓ Performance monitoring")
    print("✓ Detailed statistics and logging")
    print("✓ Graceful cache clearing")

def main():
    """Main function to run the production cache demonstration."""
    try:
        demonstrate_production_cache()
        
        print("\n" + "=" * 60)
        print("EXERCISE 4 COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Key learnings:")
        print("- Production caches need thread safety and error handling")
        print("- Multiple eviction policies serve different use cases")
        print("- Memory management prevents system resource exhaustion")
        print("- Monitoring and logging are essential for debugging")
        print("- Cache invalidation provides control over cached data")
        print("- Graceful operations ensure data integrity")
        
    except Exception as e:
        logger.error(f"Error running exercise: {e}")

if __name__ == "__main__":
    main() 