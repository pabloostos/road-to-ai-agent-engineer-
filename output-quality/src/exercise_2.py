"""
Exercise 2: Semantic Similarity Analysis
Compare responses to similar but not identical prompts to assess semantic consistency.
"""

import os
import requests
import json
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
        "max_tokens": 100
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

def generate_similar_prompts():
    """Generate a set of semantically similar prompts for testing."""
    base_prompts = [
        "What is the capital of France?",
        "Tell me about the capital city of France.",
        "Which city is the capital of France?",
        "What's the main city of France?",
        "Name the capital of France."
    ]
    
    return base_prompts

def get_responses_for_prompts(prompts):
    """Get responses for a list of prompts."""
    responses = {}
    
    print("Generating responses for similar prompts:")
    print("-" * 50)
    
    for i, prompt in enumerate(prompts, 1):
        try:
            response = call_openrouter_api(prompt)
            responses[prompt] = response
            print(f"Prompt {i}: {prompt}")
            print(f"Response: {response}")
            print()
        except Exception as e:
            print(f"Error with prompt {i}: {e}")
            responses[prompt] = "Error"
    
    return responses

def calculate_simple_similarity(response1, response2):
    """Calculate simple similarity between two responses."""
    # Convert to lowercase for comparison
    r1_lower = response1.lower()
    r2_lower = response2.lower()
    
    # Simple word overlap calculation
    words1 = set(r1_lower.split())
    words2 = set(r2_lower.split())
    
    if not words1 or not words2:
        return 0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    similarity = len(intersection) / len(union) if union else 0
    return similarity

def analyze_semantic_consistency(responses):
    """Analyze semantic consistency across responses."""
    prompts = list(responses.keys())
    consistency_scores = []
    
    print("Semantic Similarity Analysis:")
    print("-" * 50)
    
    # Compare each pair of responses
    for i in range(len(prompts)):
        for j in range(i + 1, len(prompts)):
            prompt1 = prompts[i]
            prompt2 = prompts[j]
            response1 = responses[prompt1]
            response2 = responses[prompt2]
            
            similarity = calculate_simple_similarity(response1, response2)
            consistency_scores.append(similarity)
            
            print(f"Comparing prompts {i+1} and {j+1}:")
            print(f"Prompt 1: {prompt1}")
            print(f"Prompt 2: {prompt2}")
            print(f"Similarity: {similarity:.2f}")
            print()
    
    # Calculate average consistency
    avg_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0
    
    return {
        "average_consistency": avg_consistency,
        "individual_scores": consistency_scores,
        "total_comparisons": len(consistency_scores)
    }

def generate_consistency_report(analysis_results):
    """Generate a report on semantic consistency."""
    print("SEMANTIC CONSISTENCY REPORT")
    print("=" * 50)
    print(f"Average consistency: {analysis_results['average_consistency']:.2f}")
    print(f"Total comparisons: {analysis_results['total_comparisons']}")
    
    if analysis_results['average_consistency'] > 0.7:
        print("✓ High semantic consistency detected")
    elif analysis_results['average_consistency'] > 0.4:
        print("⚠ Moderate semantic consistency detected")
    else:
        print("✗ Low semantic consistency detected")
    
    print("\nRecommendations:")
    if analysis_results['average_consistency'] < 0.5:
        print("- Consider refining prompts for better consistency")
        print("- Test with different temperature settings")
        print("- Use more specific prompt templates")
    else:
        print("- Good semantic consistency achieved")
        print("- Consider this prompt pattern for similar tasks")

def main():
    """Main function to run the semantic similarity analysis."""
    try:
        print("Exercise 2: Semantic Similarity Analysis")
        print("Testing model responses to similar prompts")
        print("=" * 60)
        
        # Generate similar prompts
        prompts = generate_similar_prompts()
        
        # Get responses for all prompts
        responses = get_responses_for_prompts(prompts)
        
        # Analyze semantic consistency
        analysis_results = analyze_semantic_consistency(responses)
        
        # Generate report
        generate_consistency_report(analysis_results)
        
        print("\nExercise completed successfully!")
        print("Key learning: Similar prompts should produce semantically consistent responses")
        
    except Exception as e:
        print(f"Error running exercise: {e}")
        print("Please check your API key and internet connection")

if __name__ == "__main__":
    main() 