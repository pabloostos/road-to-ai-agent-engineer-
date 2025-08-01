#!/usr/bin/env python3
"""
Exercise 1: Basic API Simulation

Create a prompt that simulates a GET request retrieving movie data.
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

def create_movie_api_prompt():
    """Create a prompt for simulating a GET request for movie data."""
    prompt = """You are a REST API simulator. Simulate a GET request to retrieve movie data.

Generate a JSON response with the following fields:
- movie_id (string)
- title (string) 
- genre (string)
- rating (float)
- available_on_streaming (boolean)

Return only the JSON object, no additional text.

Example response format:
{
  "movie_id": "M001",
  "title": "The Shawshank Redemption",
  "genre": "Drama",
  "rating": 9.3,
  "available_on_streaming": true
}

Generate a realistic movie response:"""
    
    return prompt

def generate_movie_response(api_key):
    """Generate a movie API response using Helsinki-NLP translation model."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "Helsinki-NLP/opus-mt-en-es"
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    # Create the prompt
    prompt = create_movie_api_prompt()
    
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
                return f"Generated Response: {generated_text}"
            else:
                return f"Unexpected response format: {result}"
        else:
            return f"API Error: {response.status_code}"
            
    except Exception as e:
        return f"Error: {e}"

def simulate_get_request(api_key):
    """Simulate a GET request for movie data."""
    print("Exercise 1: Basic API Simulation")
    print("=" * 40)
    
    # Test API connection
    print("Testing API connection...")
    success, result = test_api_connection(api_key)
    if success:
        print(f"API working: {result[:100]}...")
    else:
        print(f"API failed: {result}")
        return
    
    print("\nSimulating GET request for movie data...")
    print("-" * 40)
    
    # Generate movie response
    movie_response = generate_movie_response(api_key)
    print(f"Response: {movie_response}")
    
    print("\nExercise 1 completed!")

def main():
    """Main function."""
    api_key = load_api_key()
    if api_key:
        simulate_get_request(api_key)
    else:
        print("Please set your HUGGINGFACE_API_KEY in the .env file")

if __name__ == "__main__":
    main() 