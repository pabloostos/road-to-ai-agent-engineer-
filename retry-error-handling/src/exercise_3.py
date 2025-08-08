"""
Exercise 3: Advanced Error Handling
Implement comprehensive error handling with different strategies for different error types.

This exercise demonstrates:
1. Comprehensive exception handling
2. Different strategies for different error types
3. Graceful degradation mechanisms
4. Error classification and categorization
5. Custom error types and handling
"""

import time
import random
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any, Union, List
from enum import Enum

class ErrorType(Enum):
    """Types of errors that can occur in API calls."""
    NETWORK = "network"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    SERVER_ERROR = "server_error"
    CLIENT_ERROR = "client_error"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    UNKNOWN = "unknown"

class ErrorStrategy(Enum):
    """Strategies for handling different error types."""
    RETRY = "retry"
    FAIL_FAST = "fail_fast"
    FALLBACK = "fallback"
    DEGRADE = "degrade"

def log_event(message: str, level: str = "INFO") -> None:
    """
    Log events with timestamp and level.
    
    Args:
        message (str): Message to log
        level (str): Log level (INFO, WARNING, ERROR)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def classify_error(status_code: Optional[int], exception: Optional[Exception] = None) -> ErrorType:
    """
    Classify an error based on status code and exception.
    
    Args:
        status_code (Optional[int]): HTTP status code
        exception (Optional[Exception]): Exception that occurred
        
    Returns:
        ErrorType: Classified error type
    """
    if exception is not None:
        if isinstance(exception, requests.exceptions.Timeout):
            return ErrorType.TIMEOUT
        elif isinstance(exception, requests.exceptions.ConnectionError):
            return ErrorType.NETWORK
        elif isinstance(exception, requests.exceptions.HTTPError):
            if exception.response is not None:
                return classify_error(exception.response.status_code)
    
    if status_code is None:
        return ErrorType.UNKNOWN
    
    if status_code == 401:
        return ErrorType.AUTHENTICATION
    elif status_code == 403:
        return ErrorType.AUTHENTICATION
    elif status_code == 429:
        return ErrorType.RATE_LIMIT
    elif 400 <= status_code < 500:
        return ErrorType.CLIENT_ERROR
    elif 500 <= status_code < 600:
        return ErrorType.SERVER_ERROR
    else:
        return ErrorType.UNKNOWN

def get_error_strategy(error_type: ErrorType) -> ErrorStrategy:
    """
    Determine the appropriate strategy for an error type.
    
    Args:
        error_type (ErrorType): The type of error
        
    Returns:
        ErrorStrategy: Strategy to use for this error
    """
    strategy_map = {
        ErrorType.NETWORK: ErrorStrategy.RETRY,
        ErrorType.TIMEOUT: ErrorStrategy.RETRY,
        ErrorType.RATE_LIMIT: ErrorStrategy.RETRY,
        ErrorType.SERVER_ERROR: ErrorStrategy.RETRY,
        ErrorType.AUTHENTICATION: ErrorStrategy.FAIL_FAST,
        ErrorType.CLIENT_ERROR: ErrorStrategy.FAIL_FAST,
        ErrorType.VALIDATION: ErrorStrategy.FAIL_FAST,
        ErrorType.UNKNOWN: ErrorStrategy.FAIL_FAST
    }
    
    return strategy_map.get(error_type, ErrorStrategy.FAIL_FAST)

def calculate_backoff_delay(attempt: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """Calculate exponential backoff delay with jitter."""
    exponential_delay = base_delay * (2 ** attempt)
    capped_delay = min(exponential_delay, max_delay)
    jitter_factor = random.uniform(0.75, 1.25)
    final_delay = capped_delay * jitter_factor
    return max(final_delay, 0.1)

def handle_rate_limit(response: requests.Response) -> float:
    """
    Handle rate limit by extracting retry-after header.
    
    Args:
        response (requests.Response): HTTP response with rate limit
        
    Returns:
        float: Delay to wait before retry
    """
    retry_after = response.headers.get('Retry-After')
    if retry_after:
        try:
            return float(retry_after)
        except ValueError:
            pass
    
    # Default delay for rate limits
    return 60.0

def validate_response(response: requests.Response) -> bool:
    """
    Validate response for common issues.
    
    Args:
        response (requests.Response): HTTP response
        
    Returns:
        bool: True if response is valid, False otherwise
    """
    try:
        # Check if response is JSON
        if 'application/json' in response.headers.get('Content-Type', ''):
            response.json()
        
        # Check for empty response
        if not response.content:
            log_event("Empty response received", "WARNING")
            return False
        
        return True
    except json.JSONDecodeError:
        log_event("Invalid JSON response", "ERROR")
        return False
    except Exception as e:
        log_event(f"Response validation error: {e}", "ERROR")
        return False

def call_api_with_advanced_error_handling(url: str,
                                        max_retries: int = 3,
                                        base_delay: float = 1.0,
                                        max_delay: float = 60.0,
                                        timeout: int = 10,
                                        fallback_data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], None]:
    """
    Call an API with advanced error handling and multiple strategies.
    
    This function:
    1. Makes HTTP requests with comprehensive error handling
    2. Classifies errors and applies appropriate strategies
    3. Implements graceful degradation with fallbacks
    4. Handles rate limits with proper delays
    5. Validates responses for common issues
    
    Args:
        url (str): API endpoint URL
        max_retries (int): Maximum number of retry attempts
        base_delay (float): Base delay for exponential backoff
        max_delay (float): Maximum delay cap
        timeout (int): Request timeout in seconds
        fallback_data (Optional[Dict[str, Any]]): Fallback data if all retries fail
        
    Returns:
        Union[Dict[str, Any], None]: Response data, fallback data, or None
    """
    attempt = 0
    
    while attempt <= max_retries:
        try:
            log_event(f"Attempt {attempt + 1}/{max_retries + 1}: Making request to {url}")
            
            # Make the HTTP request
            response = requests.get(url, timeout=timeout)
            
            # Validate response
            if not validate_response(response):
                log_event("Response validation failed", "ERROR")
                return None
            
            # Check if response is successful
            if response.status_code == 200:
                log_event("SUCCESS: Request completed successfully")
                return response.json()
            
            # Classify the error
            error_type = classify_error(response.status_code)
            strategy = get_error_strategy(error_type)
            
            log_event(f"Error classified as: {error_type.value} (Strategy: {strategy.value})", "INFO")
            
            # Apply appropriate strategy
            if strategy == ErrorStrategy.RETRY:
                if attempt < max_retries:
                    # Handle rate limits specially
                    if error_type == ErrorType.RATE_LIMIT:
                        delay = handle_rate_limit(response)
                        log_event(f"RATE LIMIT: Waiting {delay}s before retry", "WARNING")
                    else:
                        delay = calculate_backoff_delay(attempt, base_delay, max_delay)
                        log_event(f"RETRYABLE ERROR: HTTP {response.status_code} - Retrying in {delay:.2f}s", "INFO")
                    
                    time.sleep(delay)
                    attempt += 1
                    continue
                else:
                    log_event(f"MAX RETRIES REACHED: HTTP {response.status_code} after {max_retries + 1} attempts", "ERROR")
                    break
            
            elif strategy == ErrorStrategy.FAIL_FAST:
                log_event(f"FAIL-FAST ERROR: HTTP {response.status_code} - Stopping immediately", "ERROR")
                return None
            
            elif strategy == ErrorStrategy.FALLBACK:
                log_event("Using fallback data due to error", "WARNING")
                return fallback_data
            
            else:
                log_event(f"Unknown strategy for error type: {error_type.value}", "ERROR")
                return None
        
        except requests.exceptions.Timeout as e:
            error_type = ErrorType.TIMEOUT
            strategy = get_error_strategy(error_type)
            
            log_event(f"TIMEOUT ERROR: {e} (Strategy: {strategy.value})", "WARNING")
            
            if strategy == ErrorStrategy.RETRY and attempt < max_retries:
                delay = calculate_backoff_delay(attempt, base_delay, max_delay)
                log_event(f"Retrying timeout error in {delay:.2f}s", "INFO")
                time.sleep(delay)
                attempt += 1
                continue
            else:
                log_event("Max retries reached for timeout", "ERROR")
                break
        
        except requests.exceptions.ConnectionError as e:
            error_type = ErrorType.NETWORK
            strategy = get_error_strategy(error_type)
            
            log_event(f"CONNECTION ERROR: {e} (Strategy: {strategy.value})", "WARNING")
            
            if strategy == ErrorStrategy.RETRY and attempt < max_retries:
                delay = calculate_backoff_delay(attempt, base_delay, max_delay)
                log_event(f"Retrying connection error in {delay:.2f}s", "INFO")
                time.sleep(delay)
                attempt += 1
                continue
            else:
                log_event("Max retries reached for connection error", "ERROR")
                break
        
        except requests.exceptions.RequestException as e:
            error_type = ErrorType.UNKNOWN
            strategy = get_error_strategy(error_type)
            
            log_event(f"REQUEST ERROR: {e} (Strategy: {strategy.value})", "ERROR")
            
            if strategy == ErrorStrategy.RETRY and attempt < max_retries:
                delay = calculate_backoff_delay(attempt, base_delay, max_delay)
                log_event(f"Retrying request error in {delay:.2f}s", "INFO")
                time.sleep(delay)
                attempt += 1
                continue
            else:
                log_event("Max retries reached for request error", "ERROR")
                break
    
    # If we get here, all retries failed
    if fallback_data is not None:
        log_event("Using fallback data after all retries failed", "WARNING")
        return fallback_data
    
    log_event("All retries failed and no fallback available", "ERROR")
    return None

def demonstrate_advanced_error_handling():
    """
    Demonstrate advanced error handling with different scenarios.
    """
    print("=" * 60)
    print("EXERCISE 3: ADVANCED ERROR HANDLING")
    print("=" * 60)
    
    # Test scenarios with different error types
    test_cases = [
        {
            "name": "Server Error (500) - Retry Strategy",
            "url": "https://httpbin.org/status/500",
            "description": "Testing retry strategy for server errors",
            "fallback": None
        },
        {
            "name": "Rate Limit (429) - Retry with Delay",
            "url": "https://httpbin.org/status/429",
            "description": "Testing rate limit handling",
            "fallback": None
        },
        {
            "name": "Authentication Error (401) - Fail Fast",
            "url": "https://httpbin.org/status/401",
            "description": "Testing fail-fast for auth errors",
            "fallback": None
        },
        {
            "name": "Client Error (400) - Fail Fast",
            "url": "https://httpbin.org/status/400",
            "description": "Testing fail-fast for client errors",
            "fallback": None
        },
        {
            "name": "Success with Fallback",
            "url": "https://httpbin.org/status/500",
            "description": "Testing fallback mechanism",
            "fallback": {"message": "Fallback data", "source": "cache"}
        },
        {
            "name": "Valid Response (200)",
            "url": "https://httpbin.org/json",
            "description": "Testing successful request",
            "fallback": None
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        print(f"Description: {test_case['description']}")
        print(f"URL: {test_case['url']}")
        if test_case['fallback']:
            print(f"Fallback: {test_case['fallback']}")
        
        # Test with advanced error handling
        result = call_api_with_advanced_error_handling(
            url=test_case['url'],
            max_retries=3,
            base_delay=1.0,
            max_delay=30.0,
            fallback_data=test_case['fallback']
        )
        
        if result is not None:
            print(f"✅ SUCCESS: Received response")
            if isinstance(result, dict):
                print(f"Response keys: {list(result.keys())}")
                if 'source' in result:
                    print(f"Source: {result['source']}")
        else:
            print(f"❌ FAILED: All retries exhausted")
        
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("EXERCISE 3 COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("Key learnings:")
    print("- Comprehensive error classification")
    print("- Different strategies for different error types")
    print("- Graceful degradation with fallbacks")
    print("- Rate limit handling with proper delays")
    print("- Response validation for common issues")
    print("- Fail-fast for non-retryable errors")

def demonstrate_error_classification():
    """
    Demonstrate error classification system.
    """
    print("\n" + "=" * 60)
    print("ERROR CLASSIFICATION DEMONSTRATION")
    print("=" * 60)
    
    # Test different error scenarios
    error_scenarios = [
        {"status_code": 200, "exception": None, "description": "Success"},
        {"status_code": 400, "exception": None, "description": "Client Error"},
        {"status_code": 401, "exception": None, "description": "Authentication Error"},
        {"status_code": 429, "exception": None, "description": "Rate Limit"},
        {"status_code": 500, "exception": None, "description": "Server Error"},
        {"status_code": None, "exception": requests.exceptions.Timeout(), "description": "Timeout"},
        {"status_code": None, "exception": requests.exceptions.ConnectionError(), "description": "Network Error"},
    ]
    
    print("Status Code | Exception | Error Type | Strategy")
    print("------------|-----------|------------|----------")
    
    for scenario in error_scenarios:
        error_type = classify_error(scenario["status_code"], scenario["exception"])
        strategy = get_error_strategy(error_type)
        
        status_str = str(scenario["status_code"]) if scenario["status_code"] else "None"
        exception_str = scenario["exception"].__class__.__name__ if scenario["exception"] else "None"
        
        print(f"{status_str:11} | {exception_str:9} | {error_type.value:10} | {strategy.value}")

def main():
    """Main function to run the advanced error handling demonstration."""
    try:
        demonstrate_advanced_error_handling()
        demonstrate_error_classification()
    except Exception as e:
        log_event(f"Error running exercise: {e}", "ERROR")

if __name__ == "__main__":
    main() 