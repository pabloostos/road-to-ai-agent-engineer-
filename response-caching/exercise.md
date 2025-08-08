# Exercise: Implementing a Python-Based AI Response Cache

## Objective
Implement a caching system that stores and retrieves AI responses to avoid redundant API calls.

---

## 1. Requirements

- **Store responses** based on unique keys (prompt + model settings).
- **Retrieve cached responses** instantly for repeated requests.
- **Handle TTL** so old responses are refreshed.
- **Demonstrate** with a mock AI API call.

---

## 2. Instructions

1. **Setup**
   - Create a Python script `ai_cache.py`.
   - Use either:
     - In-memory dictionary
     - `diskcache` (for persistence)

2. **Define a Cache Manager Class**
   ```python
   import time
   import hashlib

   class ResponseCache:
       def __init__(self, ttl=60):
           self.cache = {}
           self.ttl = ttl

       def _make_key(self, prompt, params):
           raw_key = f"{prompt}_{params}"
           return hashlib.sha256(raw_key.encode()).hexdigest()

       def get(self, prompt, params):
           key = self._make_key(prompt, params)
           if key in self.cache:
               entry = self.cache[key]
               if time.time() - entry['time'] < self.ttl:
                   return entry['response']
           return None

       def set(self, prompt, params, response):
           key = self._make_key(prompt, params)
           self.cache[key] = {"response": response, "time": time.time()}
   ```

3. **Implement Mock AI API**
   - Create a function that simulates an AI API call.
   - Add artificial delay to demonstrate caching benefits.

4. **Test the Cache**
   - Make multiple identical requests.
   - Measure response times.
   - Verify cache hits and misses.

5. **Advanced Features (Optional)**
   - Implement cache statistics (hit rate, miss rate).
   - Add cache size limits.
   - Implement cache eviction strategies.

---

## 3. Expected Output

Your implementation should demonstrate:
- **Cache hits** for repeated requests (faster response times).
- **Cache misses** for new requests (slower, but fresh data).
- **TTL expiration** (old entries become invalid).
- **Performance metrics** showing the benefits of caching.

---

## 4. Success Criteria

- ✅ Cache stores and retrieves responses correctly.
- ✅ TTL functionality works as expected.
- ✅ Performance improvement is measurable.
- ✅ Code is clean and well-documented.
- ✅ Error handling is implemented.

---

## 5. Bonus Challenges

1. **Persistent Caching**: Use `diskcache` to make cache survive restarts.
2. **Cache Statistics**: Track hit/miss rates and response times.
3. **Cache Eviction**: Implement LRU (Least Recently Used) eviction.
4. **Thread Safety**: Make cache thread-safe for concurrent access.
5. **Integration**: Integrate with real OpenRouter API calls.

---

## 6. Learning Outcomes

By completing this exercise, you will understand:
- How caching improves AI system performance.
- Best practices for cache key design.
- TTL and cache invalidation strategies.
- Trade-offs between different caching approaches.
- How to measure and optimize cache effectiveness.

--- 