"""
Exercise 1: Basic Consistency Testing
Test model responses to identical prompts with different temperature settings.
"""

import os
import requests
import json
import statistics
from dotenv import load_dotenv

def load_api_key():
    """Load OpenRouter API key from environment variables."""
    load_dotenv()
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    return api_key

def call_openrouter_api(prompt, temperature=0.1, model="openai/gpt-3.5-turbo"):
    """Call OpenRouter API with specified parameters."""
    api_key = load_api_key()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 150
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"API Error: {response.status_code}")

def test_consistency(prompt, num_tests=5, temperature=0.1):
    """Test consistency by calling the same prompt multiple times."""
    responses = []
    
    print(f"Testing consistency with temperature={temperature}")
    print(f"Prompt: {prompt}")
    print("-" * 50)
    
    for i in range(num_tests):
        try:
            response = call_openrouter_api(prompt, temperature)
            responses.append(response)
            print(f"Test {i+1}: {response[:100]}...")
        except Exception as e:
            print(f"Error in test {i+1}: {e}")
    
    return responses

def calculate_consistency_metrics(responses):
    """Calculate basic consistency metrics."""
    if len(responses) < 2:
        return {"consistency_percentage": 0, "variations": 0}
    
    # Count unique responses
    unique_responses = set(responses)
    total_responses = len(responses)
    variations = len(unique_responses)
    
    # Calculate consistency percentage
    consistency_percentage = ((total_responses - variations) / total_responses) * 100
    
    # Calculate response lengths for statistical analysis
    response_lengths = [len(response) for response in responses]
    mean_length = statistics.mean(response_lengths)
    std_length = statistics.stdev(response_lengths) if len(response_lengths) > 1 else 0
    
    return {
        "consistency_percentage": consistency_percentage,
        "variations": variations,
        "total_responses": total_responses,
        "mean_length": mean_length,
        "std_length": std_length,
        "unique_responses": list(unique_responses)
    }

def run_consistency_comparison():
    """Compare consistency between deterministic and non-deterministic settings."""
    test_prompt = "What is the capital of France and what is something interesting about it? Provide a brief answer."
    
    print("Basic Consistency Testing")
    print("=" * 50)
    
    # Test with temperature = 0 (deterministic)
    print("\n1. Testing with temperature = 0 (deterministic)")
    deterministic_responses = test_consistency(test_prompt, num_tests=3, temperature=0)
    deterministic_metrics = calculate_consistency_metrics(deterministic_responses)
    
    print(f"\nDeterministic Results:")
    print(f"- Consistency: {deterministic_metrics['consistency_percentage']:.1f}%")
    print(f"- Variations: {deterministic_metrics['variations']}")
    print(f"- Mean length: {deterministic_metrics['mean_length']:.1f} characters")
    print(f"- Std deviation: {deterministic_metrics['std_length']:.1f}")
    
    # Test with temperature = 0.7 (non-deterministic)
    print("\n2. Testing with temperature = 0.7 (non-deterministic)")
    nondeterministic_responses = test_consistency(test_prompt, num_tests=3, temperature=0.7)
    nondeterministic_metrics = calculate_consistency_metrics(nondeterministic_responses)
    
    print(f"\nNon-deterministic Results:")
    print(f"- Consistency: {nondeterministic_metrics['consistency_percentage']:.1f}%")
    print(f"- Variations: {nondeterministic_metrics['variations']}")
    print(f"- Mean length: {nondeterministic_metrics['mean_length']:.1f} characters")
    print(f"- Std deviation: {nondeterministic_metrics['std_length']:.1f}")
    
    # Comparison summary
    print("\n" + "=" * 50)
    print("COMPARISON SUMMARY")
    print("=" * 50)
    print(f"Deterministic (temp=0): {deterministic_metrics['consistency_percentage']:.1f}% consistency")
    print(f"Non-deterministic (temp=0.7): {nondeterministic_metrics['consistency_percentage']:.1f}% consistency")
    
    if deterministic_metrics['consistency_percentage'] > nondeterministic_metrics['consistency_percentage']:
        print("✓ Deterministic setting shows higher consistency (as expected)")
    else:
        print("⚠ Unexpected: Non-deterministic setting shows higher consistency")
    
    return {
        "deterministic": deterministic_metrics,
        "nondeterministic": nondeterministic_metrics
    }

def main():
    """Main function to run the consistency testing exercise."""
    try:
        print("Exercise 1: Basic Consistency Testing")
        print("Testing model responses with different temperature settings")
        print("=" * 60)
        
        results = run_consistency_comparison()
        
        print("\nExercise completed successfully!")
        print("Key learning: Temperature parameter significantly affects response consistency")
        
    except Exception as e:
        print(f"Error running exercise: {e}")
        print("Please check your API key and internet connection")

if __name__ == "__main__":
    main() 