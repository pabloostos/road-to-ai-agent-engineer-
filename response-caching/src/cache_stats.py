"""
Exercise 3: Cache Performance Monitoring
Implement cache statistics and monitoring for optimization insights.

This exercise demonstrates:
1. Hit/miss rate calculation
2. Response time tracking
3. Cache efficiency metrics
4. Performance optimization recommendations
"""

import time
import hashlib
import json
import statistics
from typing import Dict, Any, Optional, List
from collections import defaultdict

class CachePerformanceMonitor:
    """
    A comprehensive cache performance monitoring system.
    
    This class implements:
    - Detailed hit/miss rate tracking
    - Response time analysis
    - Cache efficiency metrics
    - Performance optimization recommendations
    """
    
    def __init__(self):
        """Initialize the performance monitoring system."""
        self.stats = {
            "total_requests": 0,
            "hits": 0,
            "misses": 0,
            "response_times": {
                "cache_hits": [],
                "cache_misses": [],
                "api_calls": []
            },
            "cache_size_history": [],
            "hit_rate_history": [],
            "performance_by_key": defaultdict(lambda: {
                "requests": 0,
                "hits": 0,
                "misses": 0,
                "avg_response_time": 0
            })
        }
        
        self.start_time = time.time()
        self.session_id = int(time.time())
    
    def record_request(self, key: str, is_hit: bool, response_time: float, 
                      cache_size: int = 0, api_call_time: float = 0):
        """
        Record a cache request with detailed metrics.
        
        Args:
            key (str): Cache key
            is_hit (bool): Whether it was a cache hit
            response_time (float): Time taken to get response
            cache_size (int): Current cache size
            api_call_time (float): Time taken for API call (if miss)
        """
        self.stats["total_requests"] += 1
        
        # Update basic stats
        if is_hit:
            self.stats["hits"] += 1
            self.stats["response_times"]["cache_hits"].append(response_time)
        else:
            self.stats["misses"] += 1
            self.stats["response_times"]["cache_misses"].append(response_time)
            if api_call_time > 0:
                self.stats["response_times"]["api_calls"].append(api_call_time)
        
        # Update per-key statistics
        key_stats = self.stats["performance_by_key"][key]
        key_stats["requests"] += 1
        if is_hit:
            key_stats["hits"] += 1
        else:
            key_stats["misses"] += 1
        
        # Update average response time for this key
        if key_stats["requests"] == 1:
            key_stats["avg_response_time"] = response_time
        else:
            # Calculate running average
            key_stats["avg_response_time"] = (
                (key_stats["avg_response_time"] * (key_stats["requests"] - 1) + response_time) 
                / key_stats["requests"]
            )
        
        # Record cache size history
        if cache_size > 0:
            self.stats["cache_size_history"].append({
                "timestamp": time.time(),
                "size": cache_size
            })
        
        # Record hit rate history
        current_hit_rate = (self.stats["hits"] / self.stats["total_requests"]) * 100
        self.stats["hit_rate_history"].append({
            "timestamp": time.time(),
            "hit_rate": current_hit_rate
        })
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive cache performance statistics.
        
        Returns:
            Dict[str, Any]: Detailed performance metrics
        """
        total = self.stats["total_requests"]
        hits = self.stats["hits"]
        misses = self.stats["misses"]
        
        # Calculate hit rate
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        # Calculate response time statistics
        cache_hit_times = self.stats["response_times"]["cache_hits"]
        cache_miss_times = self.stats["response_times"]["cache_misses"]
        api_call_times = self.stats["response_times"]["api_calls"]
        
        # Calculate averages and percentiles
        avg_cache_hit_time = statistics.mean(cache_hit_times) if cache_hit_times else 0
        avg_cache_miss_time = statistics.mean(cache_miss_times) if cache_miss_times else 0
        avg_api_call_time = statistics.mean(api_call_times) if api_call_times else 0
        
        # Calculate percentiles for response times
        p95_cache_hit = statistics.quantiles(cache_hit_times, n=20)[-1] if len(cache_hit_times) > 1 else 0
        p95_cache_miss = statistics.quantiles(cache_miss_times, n=20)[-1] if len(cache_miss_times) > 1 else 0
        
        # Calculate session duration
        session_duration = time.time() - self.start_time
        
        # Calculate requests per second
        requests_per_second = total / session_duration if session_duration > 0 else 0
        
        # Find most requested keys
        key_performance = self.stats["performance_by_key"]
        most_requested_keys = sorted(
            key_performance.items(), 
            key=lambda x: x[1]["requests"], 
            reverse=True
        )[:5]
        
        return {
            "basic_stats": {
                "total_requests": total,
                "hits": hits,
                "misses": misses,
                "hit_rate": hit_rate,
                "session_duration": session_duration,
                "requests_per_second": requests_per_second
            },
            "response_times": {
                "avg_cache_hit": avg_cache_hit_time,
                "avg_cache_miss": avg_cache_miss_time,
                "avg_api_call": avg_api_call_time,
                "p95_cache_hit": p95_cache_hit,
                "p95_cache_miss": p95_cache_miss,
                "speedup_factor": avg_api_call_time / avg_cache_hit_time if avg_cache_hit_time > 0 else 0
            },
            "performance_insights": {
                "most_requested_keys": most_requested_keys,
                "cache_efficiency": self._calculate_cache_efficiency(),
                "optimization_recommendations": self._generate_recommendations()
            }
        }
    
    def _calculate_cache_efficiency(self) -> Dict[str, Any]:
        """Calculate cache efficiency metrics."""
        total = self.stats["total_requests"]
        hits = self.stats["hits"]
        
        if total == 0:
            return {"efficiency_score": 0, "status": "No data"}
        
        # Calculate efficiency score (0-100)
        hit_rate = (hits / total) * 100
        
        # Calculate cost savings (assuming API calls cost money)
        api_calls_saved = hits
        cost_savings_percentage = (api_calls_saved / total) * 100 if total > 0 else 0
        
        # Determine efficiency status
        if hit_rate >= 80:
            status = "Excellent"
        elif hit_rate >= 60:
            status = "Good"
        elif hit_rate >= 40:
            status = "Fair"
        else:
            status = "Poor"
        
        return {
            "efficiency_score": hit_rate,
            "status": status,
            "api_calls_saved": api_calls_saved,
            "cost_savings_percentage": cost_savings_percentage
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations based on performance data."""
        recommendations = []
        
        total = self.stats["total_requests"]
        hits = self.stats["hits"]
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        # Analyze hit rate
        if hit_rate < 30:
            recommendations.append("Low hit rate: Consider increasing cache size or TTL")
        elif hit_rate < 50:
            recommendations.append("Moderate hit rate: Review cache key strategy")
        
        # Analyze response times
        cache_hit_times = self.stats["response_times"]["cache_hits"]
        if cache_hit_times:
            avg_hit_time = statistics.mean(cache_hit_times)
            if avg_hit_time > 0.1:  # More than 100ms
                recommendations.append("Slow cache hits: Consider optimizing cache storage")
        
        # Analyze request patterns
        key_performance = self.stats["performance_by_key"]
        if len(key_performance) > 1000:
            recommendations.append("Many unique keys: Consider cache key optimization")
        
        # Check for hot keys
        hot_keys = [k for k, v in key_performance.items() if v["requests"] > 10]
        if len(hot_keys) < len(key_performance) * 0.1:  # Less than 10% are hot
            recommendations.append("Low key reuse: Consider pre-warming frequently used data")
        
        if not recommendations:
            recommendations.append("Cache performance looks good!")
        
        return recommendations

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

class MonitoredCache:
    """
    A cache with integrated performance monitoring.
    """
    
    def __init__(self, ttl: int = 60):
        """Initialize cache with monitoring."""
        self.cache = {}
        self.ttl = ttl
        self.monitor = CachePerformanceMonitor()
    
    def _make_key(self, prompt: str, params: Dict[str, Any]) -> str:
        """Generate cache key."""
        params_str = json.dumps(params, sort_keys=True)
        raw_key = f"{prompt}_{params_str}"
        return hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
    
    def get(self, prompt: str, params: Dict[str, Any]) -> Optional[str]:
        """Get cached response with performance monitoring."""
        key = self._make_key(prompt, params)
        start_time = time.time()
        
        if key in self.cache:
            entry = self.cache[key]
            current_time = time.time()
            
            if current_time - entry['time'] < self.ttl:
                # Cache HIT
                response_time = time.time() - start_time
                self.monitor.record_request(key, True, response_time, len(self.cache))
                print(f"Cache HIT for key: {key[:8]}...")
                return entry['response']
            else:
                # Cache EXPIRED
                del self.cache[key]
        
        # Cache MISS
        response_time = time.time() - start_time
        self.monitor.record_request(key, False, response_time, len(self.cache))
        print(f"Cache MISS for key: {key[:8]}...")
        return None
    
    def set(self, prompt: str, params: Dict[str, Any], response: str) -> None:
        """Set cached response."""
        key = self._make_key(prompt, params)
        self.cache[key] = {
            "response": response,
            "time": time.time()
        }
        print(f"Cached response for key: {key[:8]}...")
    
    def get_stats(self):
        """Get comprehensive performance statistics."""
        return self.monitor.get_comprehensive_stats()

def demonstrate_performance_monitoring():
    """
    Demonstrate comprehensive cache performance monitoring.
    """
    print("=" * 60)
    print("EXERCISE 3: CACHE PERFORMANCE MONITORING")
    print("=" * 60)
    
    # Initialize monitored cache
    cache = MonitoredCache(ttl=30)
    test_params = {"model": "gpt-3.5-turbo", "temperature": 0.1}
    
    print("\n1. Testing with varied request patterns:")
    print("-" * 40)
    
    # Create varied request patterns
    prompts = [
        "What is the capital of France?",  # Will be repeated
        "What's the weather like?",        # Will be repeated
        "What is 2 + 2?",                  # Will be repeated
        "Tell me about AI",                # Unique
        "Explain machine learning",        # Unique
        "What is the capital of France?",  # Repeat
        "What's the weather like?",        # Repeat
        "What is 2 + 2?",                  # Repeat
        "New unique prompt 1",             # Unique
        "New unique prompt 2",             # Unique
        "What is the capital of France?",  # Repeat again
    ]
    
    # Process all requests
    for i, prompt in enumerate(prompts, 1):
        print(f"\nRequest {i}: {prompt}")
        
        cached_response = cache.get(prompt, test_params)
        
        if cached_response is None:
            # Cache miss: Make API call
            api_start = time.time()
            response = mock_ai_api_call(prompt, test_params)
            api_time = time.time() - api_start
            
            cache.set(prompt, test_params, response)
            
            # Record API call time
            cache.monitor.record_request(
                cache._make_key(prompt, test_params), 
                False, 0, len(cache.cache), api_time
            )
            
            print(f"Response: {response}")
            print(f"API call time: {api_time:.2f}s")
        else:
            print(f"Response: {cached_response}")
    
    print("\n2. Comprehensive Performance Analysis:")
    print("-" * 40)
    
    stats = cache.get_stats()
    
    # Display basic stats
    basic = stats["basic_stats"]
    print(f"Total requests: {basic['total_requests']}")
    print(f"Cache hits: {basic['hits']}")
    print(f"Cache misses: {basic['misses']}")
    print(f"Hit rate: {basic['hit_rate']:.1f}%")
    print(f"Session duration: {basic['session_duration']:.1f}s")
    print(f"Requests per second: {basic['requests_per_second']:.2f}")
    
    # Display response time analysis
    response_times = stats["response_times"]
    print(f"\nResponse Time Analysis:")
    print(f"Average cache hit time: {response_times['avg_cache_hit']:.4f}s")
    print(f"Average cache miss time: {response_times['avg_cache_miss']:.4f}s")
    print(f"Average API call time: {response_times['avg_api_call']:.2f}s")
    print(f"95th percentile cache hit: {response_times['p95_cache_hit']:.4f}s")
    print(f"Speedup factor: {response_times['speedup_factor']:.1f}x")
    
    # Display efficiency analysis
    efficiency = stats["performance_insights"]["cache_efficiency"]
    print(f"\nCache Efficiency:")
    print(f"Efficiency score: {efficiency['efficiency_score']:.1f}%")
    print(f"Status: {efficiency['status']}")
    print(f"API calls saved: {efficiency['api_calls_saved']}")
    print(f"Cost savings: {efficiency['cost_savings_percentage']:.1f}%")
    
    # Display most requested keys
    most_requested = stats["performance_insights"]["most_requested_keys"]
    print(f"\nMost Requested Keys:")
    for i, (key, key_stats) in enumerate(most_requested, 1):
        print(f"{i}. Key {key[:8]}... - {key_stats['requests']} requests, "
              f"{key_stats['hits']} hits, {key_stats['misses']} misses")
    
    # Display recommendations
    recommendations = stats["performance_insights"]["optimization_recommendations"]
    print(f"\nOptimization Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    
    print("\n3. Performance Trends:")
    print("-" * 40)
    
    # Show hit rate progression
    hit_rate_history = cache.monitor.stats["hit_rate_history"]
    if len(hit_rate_history) > 1:
        initial_rate = hit_rate_history[0]["hit_rate"]
        final_rate = hit_rate_history[-1]["hit_rate"]
        print(f"Hit rate progression: {initial_rate:.1f}% → {final_rate:.1f}%")
    
    # Show cache size trends
    cache_size_history = cache.monitor.stats["cache_size_history"]
    if cache_size_history:
        initial_size = cache_size_history[0]["size"]
        final_size = cache_size_history[-1]["size"]
        print(f"Cache size progression: {initial_size} → {final_size} entries")

def main():
    """Main function to run the performance monitoring demonstration."""
    try:
        demonstrate_performance_monitoring()
        
        print("\n" + "=" * 60)
        print("EXERCISE 3 COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Key learnings:")
        print("- Comprehensive monitoring provides optimization insights")
        print("- Hit rate analysis helps identify cache effectiveness")
        print("- Response time tracking reveals performance bottlenecks")
        print("- Recommendations guide cache optimization strategies")
        print("- Performance trends help predict cache behavior")
        
    except Exception as e:
        print(f"Error running exercise: {e}")

if __name__ == "__main__":
    main() 