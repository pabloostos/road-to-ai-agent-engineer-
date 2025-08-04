# Error Handling Templates
# Week 1 - Road to AI Agent Engineer

import requests
from typing import Dict, Any, Optional

def safe_api_call(func, *args, **kwargs):
    """Safely call API functions with error handling."""
    try:
        return func(*args, **kwargs)
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

def validate_input(data: Any, required_fields: list = None) -> bool:
    """Validate input data."""
    if not data:
        return False
    
    if required_fields:
        for field in required_fields:
            if field not in data:
                return False
    
    return True

def handle_json_error(json_string: str) -> Optional[Dict[str, Any]]:
    """Handle JSON parsing errors."""
    try:
        import json
        return json.loads(json_string)
    except json.JSONDecodeError:
        return None

def create_error_response(error_type: str, message: str) -> Dict[str, Any]:
    """Create a standardized error response."""
    return {
        "success": False,
        "error_type": error_type,
        "message": message
    }

def retry_on_failure(func, max_retries: int = 3):
    """Retry function on failure."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            continue 