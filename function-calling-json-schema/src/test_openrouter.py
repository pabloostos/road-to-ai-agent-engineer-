#!/usr/bin/env python3
"""
Simple test for OpenRouter API connection.
"""

import os
import requests
from dotenv import load_dotenv

def load_api_key():
    """Load API key from environment."""
    load_dotenv()
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found!")
        return None
    
    return api_key

def test_connection(api_key):
    """Test basic connection to OpenRouter."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say hello"}
        ],
        "max_tokens": 20
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            return True, message
        else:
            return False, f"Error: {response.status_code}"
            
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Main function."""
    print("Testing OpenRouter Connection")
    print("=" * 30)
    
    api_key = load_api_key()
    if not api_key:
        return
    
    success, result = test_connection(api_key)
    if success:
        print(f"Connection successful: {result}")
    else:
        print(f"Connection failed: {result}")

if __name__ == "__main__":
    main() 