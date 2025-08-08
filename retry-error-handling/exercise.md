# Exercise: Implementing a Retry + Error Handling Wrapper for an AI API

## Objective

You will build a Python wrapper function for an LLM API call that includes:

- Configurable retries
- Exception handling
- Logging of attempts and failures

## Step-by-Step Instructions

### 1. Requirements

- Python 3.8+
- requests (or httpx)
- An AI API endpoint (you can mock this with httpbin.org/status/500 for testing)

### 2. Functional Requirements

The wrapper must:

- Accept `max_retries` and `delay_seconds` parameters.
- Retry only on:
  - Network errors
  - HTTP status codes 5xx and 429
- Log each attempt with timestamp and error.
- Stop retrying after the limit is reached.
- Return either:
  - Successful response data
  - Error message after exhausting retries

### 3. Starter Code

```python
import time
import requests
from datetime import datetime

def call_api_with_retry(url, max_retries=3, delay_seconds=2):
    attempt = 0
    while attempt <= max_retries:
        try:
            response = requests.get(url, timeout=5)
            
            # If response is successful, return it
            if response.status_code == 200:
                return response.json()
            
            # Retry on 5xx or rate limits
            if response.status_code in [429] or (500 <= response.status_code < 600):
                log_event(f"Retry {attempt+1}: HTTP {response.status_code}")
                time.sleep(delay_seconds)
                attempt += 1
                continue
            
            # For other errors, stop retrying
            log_event(f"Non-retryable error: HTTP {response.status_code}")
            return None
        
        except requests.exceptions.RequestException as e:
            log_event(f"Exception: {e} - retrying...")
            time.sleep(delay_seconds)
            attempt += 1

    log_event("Max retries reached. Request failed.")
    return None

def log_event(message):
    print(f"[{datetime.now()}] {message}")

# Test with a mock server
if __name__ == "__main__":
    result = call_api_with_retry("https://httpbin.org/status/500")
    print(result)
```

### 4. Tasks

Modify the function to:

- Use exponential backoff with jitter.
- Allow specifying HTTP methods (GET, POST).
- Integrate with a real AI API endpoint (or mock server).
- Add logging to a file instead of just console.

### 5. Expected Output (Example Log)

```
[2025-08-08 09:32:01] Retry 1: HTTP 500
[2025-08-08 09:32:03] Retry 2: HTTP 500
[2025-08-08 09:32:07] Retry 3: HTTP 500
[2025-08-08 09:32:07] Max retries reached. Request failed.
```

## Exercise Structure

### Exercise 1: Basic Retry Mechanism
- Implement basic retry logic with fixed delay
- Handle common HTTP status codes
- Basic logging to console

### Exercise 2: Exponential Backoff with Jitter
- Implement exponential backoff strategy
- Add jitter to prevent thundering herd
- Enhanced error classification

### Exercise 3: Advanced Error Handling
- Comprehensive exception handling
- Different error types and strategies
- Graceful degradation

### Exercise 4: Production-Ready Wrapper
- File-based logging
- Configurable parameters
- Integration with real AI APIs
- Monitoring and metrics

## Success Criteria

- ✅ Retry mechanism works with different HTTP status codes
- ✅ Exponential backoff with jitter is implemented
- ✅ Comprehensive error handling and logging
- ✅ Configurable parameters for different use cases
- ✅ Integration with real AI API endpoints
- ✅ Production-ready logging and monitoring 