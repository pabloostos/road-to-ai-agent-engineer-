#!/usr/bin/env python3
"""
Exercise 3: Simulate a Structured API Error

Construct a prompt that simulates a server error response when a required parameter is missing.
Using Hugging Face Helsinki-NLP translation model for demonstration.
"""

import os
import json
import requests
from dotenv import load_dotenv

def load_api_key():
    """Load the Hugging Face API key from environment variables."""
    load_dotenv()
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not api_key:
        print("Error: HUGGINGFACE_API_KEY not found!")
        print("Make sure you have a .env file with your API key")
        return None
    
    return api_key

def test_api_connection(api_key):
    """Test the API connection using Helsinki-NLP translation model."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "Helsinki-NLP/opus-mt-en-es"
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs": "Hello world"}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if 'translation_text' in result[0]:
                    return True, result[0]['translation_text']
                elif 'generated_text' in result[0]:
                    return True, result[0]['generated_text']
                else:
                    return True, str(result[0])
            else:
                return True, str(result)
        else:
            return False, f"API Error: {response.status_code}"
            
    except Exception as e:
        return False, f"Error: {e}"

def create_error_simulation_prompt():
    """Create a prompt for simulating a structured API error response."""
    prompt = """You are a REST API simulator. Simulate a server error response when a required parameter is missing from a POST request.

Generate a JSON error response with the following structure:
- status_code (number): HTTP status code (e.g., 422)
- error (string): Descriptive error message

Return only the JSON object, no additional text.

Example error response format:
{
  "status_code": 422,
  "error": "Missing required field: 'email'"
}

Generate a realistic API error response:"""
    
    return prompt

def generate_error_response(api_key):
    """Generate an API error response using Helsinki-NLP translation model."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "Helsinki-NLP/opus-mt-en-es"
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    # Create the prompt
    prompt = create_error_simulation_prompt()
    
    payload = {"inputs": prompt}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if 'translation_text' in result[0]:
                    generated_text = result[0]['translation_text']
                elif 'generated_text' in result[0]:
                    generated_text = result[0]['generated_text']
                else:
                    generated_text = str(result[0])
                return f"Generated Error Response: {generated_text}"
            else:
                return f"Unexpected response format: {result}"
        else:
            return f"API Error: {response.status_code}"
            
    except Exception as e:
        return f"Error: {e}"

def simulate_error_response(api_key):
    """Simulate a structured API error response."""
    print("Exercise 3: Simulate a Structured API Error")
    print("=" * 45)
    
    # Test API connection
    print("Testing API connection...")
    success, result = test_api_connection(api_key)
    if success:
        print(f"API working: {result[:100]}...")
    else:
        print(f"API failed: {result}")
        return
    
    print("\nSimulating API error response...")
    print("-" * 40)
    
    # Generate error response
    error_response = generate_error_response(api_key)
    print(f"Error Response: {error_response}")
    
    print("\nExercise 3 completed!")

def main():
    """Main function."""
    api_key = load_api_key()
    if api_key:
        simulate_error_response(api_key)
    else:
        print("Please set your HUGGINGFACE_API_KEY in the .env file")

if __name__ == "__main__":
    main() 