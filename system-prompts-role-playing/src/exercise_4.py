#!/usr/bin/env python3
"""
Exercise 4: Multi-Role System

Create a system that can switch between different roles seamlessly.
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

def create_roles():
    """Create multiple related roles."""
    roles = {
        "medical_expert": {
            "name": "Dr. Elena Rodriguez",
            "role": "Expert Medical Researcher",
            "system_prompt": """You are Dr. Elena Rodriguez, an Expert Medical Researcher.
            Always respond as a medical professional with expertise in AI and healthcare.
            Be professional, compassionate, and educational in your responses."""
        },
        "tech_expert": {
            "name": "Alex Chen",
            "role": "Senior Software Engineer",
            "system_prompt": """You are Alex Chen, a Senior Software Engineer.
            Always respond as a tech professional with expertise in software development.
            Be technical, helpful, and solution-oriented in your responses."""
        },
        "creative_expert": {
            "name": "Maria Santos",
            "role": "Creative Director",
            "system_prompt": """You are Maria Santos, a Creative Director.
            Always respond as a creative professional with expertise in design and innovation.
            Be imaginative, inspiring, and artistic in your responses."""
        }
    }
    return roles

def generate_role_response(role, user_input, api_key):
    """Generate response for a specific role."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "meta-llama/Llama-3.1-8B-Instruct"
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    parameters = {
        "max_new_tokens": 300,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.95,
        "return_full_text": False,
        "do_sample": True
    }
    
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>{role['system_prompt']}<|eot_id|><|start_header_id|>user<|end_header_id|>{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    
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

def test_role_switching(api_key):
    """Test switching between different roles."""
    print("Exercise 4: Multi-Role System")
    print("=" * 40)
    
    if not api_key:
        return
    
    # Create roles
    roles = create_roles()
    print(f"Created {len(roles)} roles:")
    for role_id, role in roles.items():
        print(f"  - {role['name']} ({role['role']})")
    
    # Test scenarios
    test_scenarios = [
        "Hello, how are you?",
        "What's your expertise?",
        "Can you help me with a problem?",
        "What's your approach to challenges?"
    ]
    
    print(f"\nTesting role switching with {len(test_scenarios)} scenarios:")
    print("=" * 50)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nScenario {i}: {scenario}")
        print("-" * 30)
        
        for role_id, role in roles.items():
            print(f"\n{role['name']} ({role['role']}):")
            response = generate_role_response(role, scenario, api_key)
            print(f"Response: {response}")
    
    print("\nExercise 4 completed!")

def main():
    """Main function."""
    api_key = load_api_key()
    test_role_switching(api_key)

if __name__ == "__main__":
    main()
