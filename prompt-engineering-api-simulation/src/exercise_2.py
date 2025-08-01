#!/usr/bin/env python3
"""
Exercise 2: Create a POST Payload

Design a prompt that generates a POST request payload for creating a new customer record.
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

def create_customer_post_prompt():
    """Create a prompt for simulating a POST request payload for customer creation."""
    prompt = """You are a REST API simulator. Create a POST request payload for creating a new customer record.

Generate a JSON payload with the following required fields:
- customer_id (string)
- name (string)
- email (string)
- phone (string)
- subscribed_to_newsletter (boolean)

Return only the JSON object, no additional text.

Example payload format:
{
  "customer_id": "CUST001",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-123-4567",
  "subscribed_to_newsletter": true
}

Generate a realistic customer payload:"""
    
    return prompt

def generate_customer_payload(api_key):
    """Generate a customer POST payload using Helsinki-NLP translation model."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "Helsinki-NLP/opus-mt-en-es"
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    # Create the prompt
    prompt = create_customer_post_prompt()
    
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
                return f"Generated Payload: {generated_text}"
            else:
                return f"Unexpected response format: {result}"
        else:
            return f"API Error: {response.status_code}"
            
    except Exception as e:
        return f"Error: {e}"

def simulate_post_request(api_key):
    """Simulate a POST request payload for customer creation."""
    print("Exercise 2: Create a POST Payload")
    print("=" * 40)
    
    # Test API connection
    print("Testing API connection...")
    success, result = test_api_connection(api_key)
    if success:
        print(f"API working: {result[:100]}...")
    else:
        print(f"API failed: {result}")
        return
    
    print("\nSimulating POST request payload for customer creation...")
    print("-" * 40)
    
    # Generate customer payload
    customer_payload = generate_customer_payload(api_key)
    print(f"Payload: {customer_payload}")
    
    print("\nExercise 2 completed!")

def main():
    """Main function."""
    api_key = load_api_key()
    if api_key:
        simulate_post_request(api_key)
    else:
        print("Please set your HUGGINGFACE_API_KEY in the .env file")

if __name__ == "__main__":
    main()
