"""
Exercise 2: Exponential Backoff with Jitter
Implement exponential backoff with jitter for more sophisticated retry strategies.

This exercise demonstrates:
1. Exponential backoff strategy (1s → 2s → 4s → 8s)
2. Jitter to prevent thundering herd problem
3. Enhanced error classification
4. Configurable backoff parameters
"""

import time
import random
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

def calculate_backoff_delay(attempt: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """
    Calculate exponential backoff delay with jitter.
    
    This function:
    1. Calculates exponential delay: base_delay * (2^attempt)
    2. Caps the delay at max_delay
    3. Adds jitter (±25% random variation)
    4. Ensures minimum delay of 0.1 seconds
    
    Args:
        attempt (int): Current attempt number (0-based)
        base_delay (float): Base delay in seconds
        max_delay (float): Maximum delay in seconds
        
    Returns:
        float: Calculated delay in seconds
    """
    # Calculate exponential delay
    exponential_delay = base_delay * (2 ** attempt)
    
    # Cap at maximum delay
    capped_delay = min(exponential_delay, max_delay)
    
    # Add jitter (±25% random variation)
    jitter_factor = random.uniform(0.75, 1.25)
    final_delay = capped_delay * jitter_factor
    
    # Ensure minimum delay
    return max(final_delay, 0.1)

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

def call_api_with_exponential_backoff(url: str, 
                                    max_retries: int = 3,
                                    base_delay: float = 1.0,
                                    max_delay: float = 60.0,
                                    timeout: int = 10) -> Optional[Dict[str, Any]]:
    """
    Call an API with exponential backoff and jitter.
    
    This function:
    1. Makes HTTP requests with timeout
    2. Retries on specific error types (5xx, 429)
    3. Uses exponential backoff with jitter
    4. Logs all attempts and delays
    5. Returns response data or None on failure
    
    Args:
        url (str): API endpoint URL
        max_retries (int): Maximum number of retry attempts
        base_delay (float): Base delay for exponential backoff
        max_delay (float): Maximum delay cap
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
                if attempt < max_retries:
                    # Calculate backoff delay
                    delay = calculate_backoff_delay(attempt, base_delay, max_delay)
                    log_event(f"RETRYABLE ERROR: HTTP {response.status_code} - Retrying in {delay:.2f}s (attempt {attempt + 1})")
                    
                    time.sleep(delay)
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
            if attempt < max_retries:
                delay = calculate_backoff_delay(attempt, base_delay, max_delay)
                log_event(f"TIMEOUT ERROR: {e} - Retrying in {delay:.2f}s (attempt {attempt + 1})")
                time.sleep(delay)
                attempt += 1
                continue
            else:
                log_event(f"MAX RETRIES REACHED: Timeout after {max_retries + 1} attempts")
                return None
        
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries:
                delay = calculate_backoff_delay(attempt, base_delay, max_delay)
                log_event(f"CONNECTION ERROR: {e} - Retrying in {delay:.2f}s (attempt {attempt + 1})")
                time.sleep(delay)
                attempt += 1
                continue
            else:
                log_event(f"MAX RETRIES REACHED: Connection error after {max_retries + 1} attempts")
                return None
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                delay = calculate_backoff_delay(attempt, base_delay, max_delay)
                log_event(f"REQUEST ERROR: {e} - Retrying in {delay:.2f}s (attempt {attempt + 1})")
                time.sleep(delay)
                attempt += 1
                continue
            else:
                log_event(f"MAX RETRIES REACHED: Request error after {max_retries + 1} attempts")
                return None
    
    log_event("MAX RETRIES REACHED: Request failed.")
    return None

def demonstrate_exponential_backoff():
    """
    Demonstrate exponential backoff with different scenarios.
    """
    print("=" * 60)
    print("EXERCISE 2: EXPONENTIAL BACKOFF WITH JITTER")
    print("=" * 60)
    
    # Test scenarios with different backoff configurations
    test_configs = [
        {
            "name": "Fast Backoff (Base: 0.5s, Max: 10s)",
            "base_delay": 0.5,
            "max_delay": 10.0,
            "description": "Quick retries with moderate delays"
        },
        {
            "name": "Standard Backoff (Base: 1s, Max: 30s)",
            "base_delay": 1.0,
            "max_delay": 30.0,
            "description": "Balanced retry strategy"
        },
        {
            "name": "Conservative Backoff (Base: 2s, Max: 60s)",
            "base_delay": 2.0,
            "max_delay": 60.0,
            "description": "Conservative approach for sensitive APIs"
        }
    ]
    
    test_urls = [
        "https://httpbin.org/status/500",
        "https://httpbin.org/status/429",
        "https://httpbin.org/json"
    ]
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n{i}. {config['name']}")
        print("-" * 40)
        print(f"Description: {config['description']}")
        print(f"Base Delay: {config['base_delay']}s")
        print(f"Max Delay: {config['max_delay']}s")
        
        # Test with different URLs
        for j, url in enumerate(test_urls, 1):
            print(f"\n  Test {j}: {url}")
            
            result = call_api_with_exponential_backoff(
                url=url,
                max_retries=3,
                base_delay=config['base_delay'],
                max_delay=config['max_delay']
            )
            
            if result is not None:
                print(f"  ✅ SUCCESS: Received response")
                if isinstance(result, dict):
                    print(f"  Response keys: {list(result.keys())}")
            else:
                print(f"  ❌ FAILED: All retries exhausted")
        
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("EXERCISE 2 COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("Key learnings:")
    print("- Exponential backoff reduces pressure on failing services")
    print("- Jitter prevents synchronized retry spikes")
    print("- Configurable parameters for different use cases")
    print("- Enhanced logging shows delay calculations")
    print("- Different backoff strategies for different scenarios")

def demonstrate_backoff_calculation():
    """
    Demonstrate how backoff delays are calculated.
    """
    print("\n" + "=" * 60)
    print("BACKOFF DELAY CALCULATION DEMONSTRATION")
    print("=" * 60)
    
    base_delay = 1.0
    max_delay = 30.0
    
    print(f"Base Delay: {base_delay}s")
    print(f"Max Delay: {max_delay}s")
    print(f"Max Retries: 5")
    print()
    
    print("Attempt | Exponential | Capped | With Jitter")
    print("--------|-------------|--------|------------")
    
    for attempt in range(6):
        exponential = base_delay * (2 ** attempt)
        capped = min(exponential, max_delay)
        
        # Calculate jitter for demonstration
        jitter_factor = random.uniform(0.75, 1.25)
        with_jitter = capped * jitter_factor
        
        print(f"{attempt:7d} | {exponential:11.1f} | {capped:6.1f} | {with_jitter:10.2f}")

def main():
    """Main function to run the exponential backoff demonstration."""
    try:
        demonstrate_exponential_backoff()
        demonstrate_backoff_calculation()
    except Exception as e:
        log_event(f"Error running exercise: {e}")

if __name__ == "__main__":
    main() 