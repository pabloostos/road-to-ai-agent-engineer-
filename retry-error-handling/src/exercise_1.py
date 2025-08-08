"""
Exercise 1: Basic Retry Mechanism
Implement a simple retry mechanism with fixed delay for AI API calls.

This exercise demonstrates:
1. Basic retry logic with fixed delays
2. HTTP status code handling (5xx, 429)
3. Network error handling
4. Basic console logging
"""

import time
import requests
from datetime import datetime
from typing import Optional, Dict, Any

def log_event(message: str) -> None:
    """
    Log events with timestamp.
    
    Args:
        message (str): Message to log
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def is_retryable_error(status_code: int) -> bool:
    """
    Determine if an HTTP status code should trigger a retry.
    
    Args:
        status_code (int): HTTP status code
        
    Returns:
        bool: True if error is retryable, False otherwise
    """
    # Retry on server errors (5xx) and rate limits (429)
    return status_code == 429 or (500 <= status_code < 600)

def call_api_with_retry(url: str, 
                        max_retries: int = 3, 
                        delay_seconds: int = 2,
                        timeout: int = 10) -> Optional[Dict[str, Any]]:
    """
    Call an API with basic retry mechanism.
    
    This function:
    1. Makes HTTP requests with timeout
    2. Retries on specific error types (5xx, 429)
    3. Uses fixed delay between retries
    4. Logs all attempts and errors
    5. Returns response data or None on failure
    
    Args:
        url (str): API endpoint URL
        max_retries (int): Maximum number of retry attempts
        delay_seconds (int): Fixed delay between retries
        timeout (int): Request timeout in seconds
        
    Returns:
        Optional[Dict[str, Any]]: Response data or None if all retries failed
    """
    attempt = 0
    
    while attempt <= max_retries:
        try:
            log_event(f"Attempt {attempt + 1}/{max_retries + 1}: Making request to {url}")
            
            # Make the HTTP request
            response = requests.get(url, timeout=timeout)
            
            # Check if response is successful
            if response.status_code == 200:
                log_event(f"SUCCESS: Request completed successfully")
                return response.json()
            
            # Check if error is retryable
            if is_retryable_error(response.status_code):
                log_event(f"RETRYABLE ERROR: HTTP {response.status_code} - Retrying in {delay_seconds}s...")
                
                if attempt < max_retries:
                    time.sleep(delay_seconds)
                    attempt += 1
                    continue
                else:
                    log_event(f"MAX RETRIES REACHED: HTTP {response.status_code} after {max_retries + 1} attempts")
                    return None
            else:
                # Non-retryable error (4xx except 429)
                log_event(f"NON-RETRYABLE ERROR: HTTP {response.status_code} - Stopping retries")
                return None
        
        except requests.exceptions.Timeout as e:
            log_event(f"TIMEOUT ERROR: {e} - Retrying in {delay_seconds}s...")
            if attempt < max_retries:
                time.sleep(delay_seconds)
                attempt += 1
                continue
            else:
                log_event(f"MAX RETRIES REACHED: Timeout after {max_retries + 1} attempts")
                return None
        
        except requests.exceptions.ConnectionError as e:
            log_event(f"CONNECTION ERROR: {e} - Retrying in {delay_seconds}s...")
            if attempt < max_retries:
                time.sleep(delay_seconds)
                attempt += 1
                continue
            else:
                log_event(f"MAX RETRIES REACHED: Connection error after {max_retries + 1} attempts")
                return None
        
        except requests.exceptions.RequestException as e:
            log_event(f"REQUEST ERROR: {e} - Retrying in {delay_seconds}s...")
            if attempt < max_retries:
                time.sleep(delay_seconds)
                attempt += 1
                continue
            else:
                log_event(f"MAX RETRIES REACHED: Request error after {max_retries + 1} attempts")
                return None
    
    log_event("MAX RETRIES REACHED: Request failed.")
    return None

def demonstrate_basic_retry():
    """
    Demonstrate the basic retry mechanism with different scenarios.
    """
    print("=" * 60)
    print("EXERCISE 1: BASIC RETRY MECHANISM")
    print("=" * 60)
    
    # Test scenarios
    test_cases = [
        {
            "name": "Server Error (500)",
            "url": "https://httpbin.org/status/500",
            "description": "Testing retry on server error"
        },
        {
            "name": "Rate Limit (429)",
            "url": "https://httpbin.org/status/429",
            "description": "Testing retry on rate limit"
        },
        {
            "name": "Success Case (200)",
            "url": "https://httpbin.org/json",
            "description": "Testing successful request"
        },
        {
            "name": "Client Error (400)",
            "url": "https://httpbin.org/status/400",
            "description": "Testing non-retryable client error"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        print(f"Description: {test_case['description']}")
        print(f"URL: {test_case['url']}")
        
        # Test with basic retry
        result = call_api_with_retry(
            url=test_case['url'],
            max_retries=3,
            delay_seconds=2
        )
        
        if result is not None:
            print(f"✅ SUCCESS: Received response")
            if isinstance(result, dict):
                print(f"Response keys: {list(result.keys())}")
        else:
            print(f"❌ FAILED: All retries exhausted")
        
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("EXERCISE 1 COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("Key learnings:")
    print("- Basic retry logic with fixed delays")
    print("- HTTP status code classification")
    print("- Network error handling")
    print("- Console logging for debugging")
    print("- Proper timeout handling")

def main():
    """Main function to run the basic retry demonstration."""
    try:
        demonstrate_basic_retry()
    except Exception as e:
        log_event(f"Error running exercise: {e}")

if __name__ == "__main__":
    main() 