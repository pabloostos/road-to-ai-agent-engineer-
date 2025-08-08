"""
Exercise 4: Production-Ready Wrapper
Implement a production-ready retry wrapper with file-based logging and real AI API integration.

This exercise demonstrates:
1. File-based logging system
2. Configurable parameters from environment
3. Integration with real AI APIs
4. Monitoring and metrics collection
5. Production-ready error handling
"""

import time
import random
import requests
import json
import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any, Union
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
def setup_logging(log_file: str = "retry_errors.log"):
    """
    Setup file-based logging system.
    
    Args:
        log_file (str): Path to log file
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class ProductionRetryWrapper:
    """
    A production-ready retry wrapper for AI API calls.
    
    Features:
    - File-based logging
    - Configurable parameters from environment
    - Integration with real AI APIs
    - Monitoring and metrics
    - Comprehensive error handling
    """
    
    def __init__(self):
        """Initialize the production retry wrapper."""
        # Load configuration from environment
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.base_delay = float(os.getenv('BASE_DELAY', 1.0))
        self.max_delay = float(os.getenv('MAX_DELAY', 60.0))
        self.timeout = int(os.getenv('TIMEOUT', 30))
        
        # API configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        
        # Metrics
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "retry_attempts": 0,
            "total_response_time": 0.0
        }
        
        logger.info(f"Production retry wrapper initialized with max_retries={self.max_retries}, "
                   f"base_delay={self.base_delay}s, max_delay={self.max_delay}s")
    
    def calculate_backoff_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter."""
        exponential_delay = self.base_delay * (2 ** attempt)
        capped_delay = min(exponential_delay, self.max_delay)
        jitter_factor = random.uniform(0.75, 1.25)
        final_delay = capped_delay * jitter_factor
        return max(final_delay, 0.1)
    
    def is_retryable_error(self, status_code: int) -> bool:
        """Determine if an HTTP status code should trigger a retry."""
        return status_code == 429 or (500 <= status_code < 600)
    
    def call_openai_api(self, prompt: str, model: str = "gpt-3.5-turbo") -> Optional[Dict[str, Any]]:
        """
        Call OpenAI API with retry mechanism.
        
        Args:
            prompt (str): The prompt to send
            model (str): Model to use
            
        Returns:
            Optional[Dict[str, Any]]: API response or None
        """
        if not self.openai_api_key:
            logger.error("OpenAI API key not configured")
            return None
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150
        }
        
        return self._make_request_with_retry(url, headers=headers, json=data)
    
    def call_openrouter_api(self, prompt: str, model: str = "openai/gpt-3.5-turbo") -> Optional[Dict[str, Any]]:
        """
        Call OpenRouter API with retry mechanism.
        
        Args:
            prompt (str): The prompt to send
            model (str): Model to use
            
        Returns:
            Optional[Dict[str, Any]]: API response or None
        """
        if not self.openrouter_api_key:
            logger.error("OpenRouter API key not configured")
            return None
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",
            "X-Title": "Retry Error Handling Exercise"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150
        }
        
        return self._make_request_with_retry(url, headers=headers, json=data)
    
    def call_mock_api(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Call a mock API for testing purposes.
        
        Args:
            url (str): URL to call
            
        Returns:
            Optional[Dict[str, Any]]: API response or None
        """
        return self._make_request_with_retry(url)
    
    def _make_request_with_retry(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Make an HTTP request with comprehensive retry logic.
        
        Args:
            url (str): URL to request
            **kwargs: Additional arguments for requests.post
            
        Returns:
            Optional[Dict[str, Any]]: Response data or None
        """
        attempt = 0
        start_time = time.time()
        
        self.metrics["total_requests"] += 1
        
        while attempt <= self.max_retries:
            try:
                logger.info(f"Attempt {attempt + 1}/{self.max_retries + 1}: Making request to {url}")
                
                # Make the HTTP request
                response = requests.post(url, timeout=self.timeout, **kwargs)
                
                # Check if response is successful
                if response.status_code == 200:
                    response_time = time.time() - start_time
                    self.metrics["successful_requests"] += 1
                    self.metrics["total_response_time"] += response_time
                    
                    logger.info(f"SUCCESS: Request completed in {response_time:.2f}s")
                    return response.json()
                
                # Check if error is retryable
                if self.is_retryable_error(response.status_code):
                    if attempt < self.max_retries:
                        delay = self.calculate_backoff_delay(attempt)
                        self.metrics["retry_attempts"] += 1
                        
                        logger.warning(f"RETRYABLE ERROR: HTTP {response.status_code} - Retrying in {delay:.2f}s")
                        time.sleep(delay)
                        attempt += 1
                        continue
                    else:
                        logger.error(f"MAX RETRIES REACHED: HTTP {response.status_code} after {self.max_retries + 1} attempts")
                        break
                else:
                    # Non-retryable error
                    logger.error(f"NON-RETRYABLE ERROR: HTTP {response.status_code} - Stopping retries")
                    break
            
            except requests.exceptions.Timeout as e:
                if attempt < self.max_retries:
                    delay = self.calculate_backoff_delay(attempt)
                    self.metrics["retry_attempts"] += 1
                    
                    logger.warning(f"TIMEOUT ERROR: {e} - Retrying in {delay:.2f}s")
                    time.sleep(delay)
                    attempt += 1
                    continue
                else:
                    logger.error("MAX RETRIES REACHED: Timeout after all attempts")
                    break
            
            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries:
                    delay = self.calculate_backoff_delay(attempt)
                    self.metrics["retry_attempts"] += 1
                    
                    logger.warning(f"CONNECTION ERROR: {e} - Retrying in {delay:.2f}s")
                    time.sleep(delay)
                    attempt += 1
                    continue
                else:
                    logger.error("MAX RETRIES REACHED: Connection error after all attempts")
                    break
            
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries:
                    delay = self.calculate_backoff_delay(attempt)
                    self.metrics["retry_attempts"] += 1
                    
                    logger.warning(f"REQUEST ERROR: {e} - Retrying in {delay:.2f}s")
                    time.sleep(delay)
                    attempt += 1
                    continue
                else:
                    logger.error("MAX RETRIES REACHED: Request error after all attempts")
                    break
        
        # If we get here, all retries failed
        self.metrics["failed_requests"] += 1
        logger.error("All retries failed")
        return None
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        total_requests = self.metrics["total_requests"]
        success_rate = (self.metrics["successful_requests"] / total_requests * 100) if total_requests > 0 else 0
        avg_response_time = (self.metrics["total_response_time"] / self.metrics["successful_requests"]) if self.metrics["successful_requests"] > 0 else 0
        
        return {
            **self.metrics,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time
        }

def demonstrate_production_wrapper():
    """
    Demonstrate the production-ready retry wrapper.
    """
    print("=" * 60)
    print("EXERCISE 4: PRODUCTION-READY WRAPPER")
    print("=" * 60)
    
    # Initialize the wrapper
    wrapper = ProductionRetryWrapper()
    
    # Test scenarios
    test_cases = [
        {
            "name": "Mock API - Server Error",
            "type": "mock",
            "url": "https://httpbin.org/status/500",
            "description": "Testing with mock server error"
        },
        {
            "name": "Mock API - Rate Limit",
            "type": "mock",
            "url": "https://httpbin.org/status/429",
            "description": "Testing with mock rate limit"
        },
        {
            "name": "Mock API - Success",
            "type": "mock",
            "url": "https://httpbin.org/json",
            "description": "Testing with mock success"
        }
    ]
    
    # Add real API tests if keys are configured
    if wrapper.openai_api_key:
        test_cases.append({
            "name": "OpenAI API - Simple Prompt",
            "type": "openai",
            "prompt": "What is the capital of France?",
            "description": "Testing with real OpenAI API"
        })
    
    if wrapper.openrouter_api_key:
        test_cases.append({
            "name": "OpenRouter API - Simple Prompt",
            "type": "openrouter",
            "prompt": "What is 2 + 2?",
            "description": "Testing with real OpenRouter API"
        })
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        print(f"Description: {test_case['description']}")
        
        # Execute the test
        if test_case["type"] == "mock":
            result = wrapper.call_mock_api(test_case["url"])
        elif test_case["type"] == "openai":
            result = wrapper.call_openai_api(test_case["prompt"])
        elif test_case["type"] == "openrouter":
            result = wrapper.call_openrouter_api(test_case["prompt"])
        
        if result is not None:
            print(f"✅ SUCCESS: Received response")
            if isinstance(result, dict):
                print(f"Response keys: {list(result.keys())}")
                if "choices" in result:
                    print(f"Choices: {len(result['choices'])}")
        else:
            print(f"❌ FAILED: All retries exhausted")
        
        print("-" * 40)
    
    # Display metrics
    print(f"\n" + "=" * 60)
    print("PRODUCTION METRICS")
    print("=" * 60)
    
    metrics = wrapper.get_metrics()
    
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Successful Requests: {metrics['successful_requests']}")
    print(f"Failed Requests: {metrics['failed_requests']}")
    print(f"Retry Attempts: {metrics['retry_attempts']}")
    print(f"Success Rate: {metrics['success_rate']:.1f}%")
    print(f"Average Response Time: {metrics['avg_response_time']:.2f}s")
    
    print("\n" + "=" * 60)
    print("EXERCISE 4 COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("Key learnings:")
    print("- File-based logging for production debugging")
    print("- Configurable parameters from environment variables")
    print("- Integration with real AI APIs (OpenAI, OpenRouter)")
    print("- Comprehensive metrics collection")
    print("- Production-ready error handling and monitoring")

def demonstrate_configuration():
    """
    Demonstrate configuration loading from environment.
    """
    print("\n" + "=" * 60)
    print("CONFIGURATION DEMONSTRATION")
    print("=" * 60)
    
    print("Environment Variables:")
    print(f"MAX_RETRIES: {os.getenv('MAX_RETRIES', '3 (default)')}")
    print(f"BASE_DELAY: {os.getenv('BASE_DELAY', '1.0 (default)')}")
    print(f"MAX_DELAY: {os.getenv('MAX_DELAY', '60.0 (default)')}")
    print(f"TIMEOUT: {os.getenv('TIMEOUT', '30 (default)')}")
    print(f"OPENAI_API_KEY: {'Configured' if os.getenv('OPENAI_API_KEY') else 'Not configured'}")
    print(f"OPENROUTER_API_KEY: {'Configured' if os.getenv('OPENROUTER_API_KEY') else 'Not configured'}")

def main():
    """Main function to run the production wrapper demonstration."""
    try:
        demonstrate_production_wrapper()
        demonstrate_configuration()
    except Exception as e:
        logger.error(f"Error running exercise: {e}")

if __name__ == "__main__":
    main() 