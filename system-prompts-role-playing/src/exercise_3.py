#!/usr/bin/env python3
"""
Exercise 3: Role Consistency Testing (Simplified)

Simple test of character consistency using Llama model with professional parameters.
"""

import os
import requests
from dotenv import load_dotenv

def load_api_key():
    """Load API key from environment."""
    load_dotenv()
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        print("Error: HUGGINGFACE_API_KEY not found!")
        return None
    return api_key

def test_api_connection(api_key):
    """Test API connection with Llama model."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "meta-llama/Llama-3.1-8B-Instruct"
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    parameters = {
        "max_new_tokens": 100,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.95,
        "return_full_text": False,
        "do_sample": True
    }
    
    payload = {
        "inputs": "Hello, how are you?",
        "parameters": parameters
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return True, result[0]['generated_text'].strip()
            else:
                return True, str(result)
        else:
            return False, f"API Error: {response.status_code}"
    except Exception as e:
        return False, f"Error: {e}"

def generate_character_response(character, user_input, system_prompt, api_key):
    """Generate character response using Llama model."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "meta-llama/Llama-3.1-8B-Instruct"
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    parameters = {
        "max_new_tokens": 500,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.95,
        "return_full_text": False,
        "do_sample": True
    }
    
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    
    payload = {
        "inputs": prompt,
        "parameters": parameters
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0]['generated_text'].strip()
            else:
                return str(result)
        else:
            return f"API Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def test_character_consistency(api_key):
    """Test character consistency with simple scenarios."""
    print("Exercise 3: Role Consistency Testing (Simplified)")
    print("=" * 50)
    
    # Load API key
    if not api_key:
        return
    
    # Test API connection
    print("Testing API connection...")
    success, result = test_api_connection(api_key)
    if success:
        print(f"API working: {result}")
    else:
        print(f"API failed: {result}")
        return
    
    # Define character
    character = {
        "name": "Dr. Elena Rodriguez",
        "role": "Expert Medical Researcher"
    }
    
    system_prompt = f"""You are {character['name']}, a {character['role']}. 
    Always respond as a medical professional with expertise in AI and healthcare.
    Be professional, compassionate, and educational in your responses."""
    
    # Test scenarios
    test_scenarios = [
        "Hello, how are you?",
        "Tell me about AI in healthcare",
        "What's your research focus?",
        "How do you approach patient safety?"
    ]
    
    print(f"\nTesting character: {character['name']}")
    print("=" * 40)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nScenario {i}: {scenario}")
        response = generate_character_response(character, scenario, system_prompt, api_key)
        print(f"Response: {response}")
    
    print("\nExercise 3 completed!")

def main():
    """Main function."""
    api_key = load_api_key()
    test_character_consistency(api_key)

if __name__ == "__main__":
    main()
