# Logging Templates
# Week 1 - Road to AI Agent Engineer

import logging
import json
from datetime import datetime
from typing import Dict, Any

def setup_logging(log_file: str = "app.log"):
    """Setup basic logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def log_api_call(logger, api_name: str, success: bool, response_time: float = None):
    """Log API call details."""
    status = "SUCCESS" if success else "FAILED"
    message = f"API Call: {api_name} - {status}"
    
    if response_time:
        message += f" - {response_time:.2f}s"
    
    if success:
        logger.info(message)
    else:
        logger.error(message)

def log_conversation(logger, user_input: str, response: str, role: str = ""):
    """Log conversation details."""
    logger.info(f"Conversation - Role: {role}")
    logger.info(f"User: {user_input}")
    logger.info(f"Response: {response}")

def save_to_json_log(data: Dict[str, Any], filename: str):
    """Save data to JSON log file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving log: {e}")

def log_error(logger, error_type: str, message: str, details: Dict[str, Any] = None):
    """Log error with details."""
    logger.error(f"{error_type}: {message}")
    if details:
        logger.error(f"Details: {details}") 