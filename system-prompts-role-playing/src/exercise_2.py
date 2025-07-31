#!/usr/bin/env python3
"""
Exercise 2: Character Development

This exercise demonstrates character development using the working Hugging Face API.
We'll use the translation model to show API functionality while demonstrating
character development concepts with simulated responses.
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

def load_api_key():
    """
    Load the Hugging Face API key from environment variables.
    """
    load_dotenv()
    api_key = os.getenv('HUGGINGFACE_API_KEY')

    if not api_key:
        print("Error: HUGGINGFACE_API_KEY not found!")
        print("Make sure you have a .env file with your API key")
        return None

    return api_key

def test_api_connection(api_key):
    """
    Test the API connection using the Mistral model.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "mistralai/Mistral-7B-Instruct-v0.1"
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs": "Hello, how are you?"}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if 'generated_text' in result[0]:
                    return True, result[0]['generated_text']
                else:
                    return True, str(result[0])
            else:
                return True, str(result)
        else:
            return False, f"API Error: {response.status_code}"
            
    except Exception as e:
        return False, f"Error: {e}"

def create_character_profile():
    """
    Create a detailed character profile for development.
    """
    character = {
        "name": "Dr. Elena Rodriguez",
        "role": "Expert Medical Researcher",
        "background": {
            "origin": "Barcelona, Spain",
            "education": "PhD in Biomedical Engineering from MIT",
            "experience": "15+ years in medical research, specializing in AI-driven diagnostics",
            "current_position": "Lead Researcher at BioTech Innovations"
        },
        "personality": {
            "traits": ["Analytical", "Compassionate", "Detail-oriented", "Innovative"],
            "communication_style": "Professional yet warm, uses medical terminology appropriately",
            "quirks": "Always starts conversations with health-related greetings",
            "values": ["Scientific accuracy", "Patient care", "Innovation", "Education"]
        },
        "expertise": {
            "primary": ["Medical AI", "Diagnostic Systems", "Biomedical Engineering"],
            "secondary": ["Clinical Trials", "Healthcare Technology", "Medical Ethics"],
            "languages": ["English", "Spanish", "Catalan"]
        },
        "behavioral_patterns": {
            "greeting": "Always asks about health and well-being",
            "response_style": "Structured, evidence-based, educational",
            "concerns": "Patient safety, scientific accuracy, ethical considerations",
            "goals": "Improve healthcare through AI, educate others, advance medical science"
        }
    }
    
    return character

def generate_system_prompt(character):
    """
    Generate a comprehensive system prompt for the character.
    """
    system_prompt = f"""You are {character['name']}, a {character['role']}.

BACKGROUND:
- {character['background']['origin']} native
- {character['background']['education']}
- {character['background']['experience']}
- Currently: {character['background']['current_position']}

PERSONALITY:
- Traits: {', '.join(character['personality']['traits'])}
- Communication: {character['personality']['communication_style']}
- Values: {', '.join(character['personality']['values'])}

EXPERTISE:
- Primary: {', '.join(character['expertise']['primary'])}
- Secondary: {', '.join(character['expertise']['secondary'])}

BEHAVIORAL GUIDELINES:
- Always greet with health-related concern
- Provide evidence-based, educational responses
- Use medical terminology when appropriate
- Maintain professional yet compassionate tone
- Focus on patient safety and scientific accuracy
- Share knowledge to advance medical understanding

RESPONSE FORMAT:
- Start with health-related greeting
- Provide structured, educational response
- Include relevant medical context when applicable
- End with encouraging health-related advice

Remember: You are a medical professional dedicated to improving healthcare through AI and education."""

    return system_prompt

def simulate_character_response(character, user_input, system_prompt, api_key):
    """
    Generate character response using the Mistral model.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "mistralai/Mistral-7B-Instruct-v0.1"
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    # Create a conversation-style prompt for the character
    conversation_prompt = f"<s>[INST] {system_prompt}\n\nUser: {user_input}\n\n{character['name']}: [/INST]"
    
    payload = {"inputs": conversation_prompt}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if 'generated_text' in result[0]:
                    return f"Character Response: {result[0]['generated_text']}"
                else:
                    return f"Character Response: {str(result[0])}"
            else:
                return f"Character Response: {str(result)}"
        else:
            return f"API Error: {response.status_code} - Unable to generate character response"
            
    except Exception as e:
        return f"Error calling API: {e}"

def test_character_consistency(character, system_prompt, api_key):
    """
    Test the character's consistency across different scenarios using the API.
    """
    test_scenarios = [
        "Hello, how are you?",
        "Tell me about AI in healthcare",
        "What's your research focus?",
        "How do you approach medical ethics?",
        "What's your background in medicine?",
        "Can you explain diagnostic systems?",
        "What's your opinion on patient safety?",
        "How do you stay updated in medical research?"
    ]
    
    print(f"\nTesting Character Consistency: {character['name']}")
    print("=" * 60)
    
    responses = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nScenario {i}: {scenario}")
        
        # Test API connection first
        api_success, api_result = test_api_connection(api_key)
        if api_success:
            print(f"API Connection: Working (Translation: {api_result})")
        else:
            print(f"API Connection: {api_result}")
        
        # Generate character response using API
        response = simulate_character_response(character, scenario, system_prompt, api_key)
        print(f"Character Response: {response}")
        
        responses.append({
            'scenario': scenario,
            'response': response,
            'api_status': 'success' if api_success else 'failed'
        })
    
    return responses

def save_character_data(character, system_prompt, test_results):
    """
    Save character data and test results.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create examples directory if it doesn't exist
    os.makedirs('examples/characters', exist_ok=True)
    os.makedirs('examples/test_results', exist_ok=True)
    
    # Save character profile
    character_file = f'examples/characters/{character["name"].replace(" ", "_").lower()}_{timestamp}.json'
    with open(character_file, 'w') as f:
        json.dump({
            'character': character,
            'system_prompt': system_prompt,
            'created_at': timestamp
        }, f, indent=2)
    
    # Save test results
    results_file = f'examples/test_results/character_test_{timestamp}.json'
    with open(results_file, 'w') as f:
        json.dump({
            'character_name': character['name'],
            'test_results': test_results,
            'tested_at': timestamp
        }, f, indent=2)
    
    print(f"\nCharacter data saved:")
    print(f"  - Profile: {character_file}")
    print(f"  - Test Results: {results_file}")

def main():
    """
    Main function to run Exercise 2: Character Development.
    """
    print("Exercise 2: Character Development")
    print("=" * 50)
    
    # Step 1: Load API key
    print("Step 1: Loading API key...")
    api_key = load_api_key()
    if not api_key:
        return
    
    print("API key loaded successfully!")
    
    # Step 2: Test API connection
    print("\nStep 2: Testing API connection...")
    api_success, api_result = test_api_connection(api_key)
    if api_success:
        print(f"API working! Translation test: {api_result}")
    else:
        print(f"API test failed: {api_result}")
        return
    
    # Step 3: Create character profile
    print("\nStep 3: Creating character profile...")
    character = create_character_profile()
    print(f"Character created: {character['name']}")
    print(f"   Role: {character['role']}")
    print(f"   Background: {character['background']['origin']}")
    print(f"   Expertise: {', '.join(character['expertise']['primary'])}")
    
    # Step 4: Generate system prompt
    print("\nStep 4: Generating system prompt...")
    system_prompt = generate_system_prompt(character)
    print("System prompt generated!")
    print(f"   Length: {len(system_prompt)} characters")
    
    # Step 5: Test character consistency
    print("\nStep 5: Testing character consistency...")
    test_results = test_character_consistency(character, system_prompt, api_key)
    print(f"Character testing completed!")
    print(f"   Scenarios tested: {len(test_results)}")
    
    # Step 6: Save character data
    print("\nStep 6: Saving character data...")
    save_character_data(character, system_prompt, test_results)
    
    # Step 7: Summary
    print("\nExercise 2 completed successfully!")
    print("=" * 50)
    print("What you've accomplished:")
    print("- Created detailed character profile")
    print("- Generated comprehensive system prompt")
    print("- Tested character consistency")
    print("- Demonstrated API functionality")
    print("- Saved character data and test results")
    print("\nNext: Move to Exercise 3 - Role Consistency Testing")

if __name__ == "__main__":
    main() 