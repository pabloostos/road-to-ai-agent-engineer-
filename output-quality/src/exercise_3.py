"""
Exercise 3: Quality Metrics Implementation
Implement automated metrics for evaluating response quality.
"""

import os
import requests
import json
import re
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
        "max_tokens": 200
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

def analyze_response_length(response):
    """Analyze response length and provide quality score."""
    length = len(response)
    word_count = len(response.split())
    
    # Score based on length appropriateness
    if word_count < 5:
        length_score = 0.3  # Too short
    elif word_count < 20:
        length_score = 0.7  # Short but acceptable
    elif word_count < 100:
        length_score = 1.0  # Good length
    elif word_count < 200:
        length_score = 0.8  # Long but acceptable
    else:
        length_score = 0.5  # Too long
    
    return {
        "length": length,
        "word_count": word_count,
        "length_score": length_score,
        "assessment": "Too short" if word_count < 10 else "Too long" if word_count > 150 else "Appropriate"
    }

def evaluate_coherence(response):
    """Evaluate the logical coherence of the response."""
    # Simple coherence checks
    sentences = re.split(r'[.!?]+', response)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    coherence_score = 1.0
    
    # Check for repeated words (indicates poor coherence)
    words = response.lower().split()
    if len(words) > 10:
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Only count significant words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Penalize excessive repetition
        max_freq = max(word_freq.values()) if word_freq else 1
        if max_freq > len(words) * 0.3:  # If any word appears more than 30% of the time
            coherence_score -= 0.3
    
    # Check for logical connectors
    connectors = ['because', 'therefore', 'however', 'although', 'furthermore', 'moreover']
    has_connectors = any(connector in response.lower() for connector in connectors)
    
    if has_connectors:
        coherence_score += 0.1
    else:
        coherence_score -= 0.1
    
    coherence_score = max(0.0, min(1.0, coherence_score))
    
    return {
        "coherence_score": coherence_score,
        "sentence_count": len(sentences),
        "has_logical_connectors": has_connectors,
        "assessment": "Good" if coherence_score > 0.7 else "Moderate" if coherence_score > 0.4 else "Poor"
    }

def evaluate_relevance(response, prompt):
    """Evaluate how relevant the response is to the prompt."""
    # Simple keyword matching
    prompt_words = set(prompt.lower().split())
    response_words = set(response.lower().split())
    
    # Remove common words
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can'}
    prompt_keywords = prompt_words - common_words
    response_keywords = response_words - common_words
    
    if not prompt_keywords:
        relevance_score = 0.5
    else:
        # Calculate keyword overlap
        keyword_overlap = len(prompt_keywords.intersection(response_keywords))
        relevance_score = keyword_overlap / len(prompt_keywords) if prompt_keywords else 0
    
    # Bonus for comprehensive response
    if len(response_words) > len(prompt_words) * 2:
        relevance_score += 0.1
    
    relevance_score = min(1.0, relevance_score)
    
    return {
        "relevance_score": relevance_score,
        "keyword_overlap": keyword_overlap if 'keyword_overlap' in locals() else 0,
        "total_keywords": len(prompt_keywords),
        "assessment": "Highly relevant" if relevance_score > 0.8 else "Relevant" if relevance_score > 0.5 else "Somewhat relevant" if relevance_score > 0.3 else "Not relevant"
    }

def evaluate_faithfulness(response, prompt):
    """Evaluate if the response stays faithful to the prompt without hallucination."""
    # Check if response contains specific factual claims that weren't in the prompt
    factual_indicators = ['according to', 'studies show', 'research indicates', 'experts say', 'it is proven']
    has_unsupported_facts = any(indicator in response.lower() for indicator in factual_indicators)
    
    # Check for hedging language (indicates uncertainty)
    hedging_words = ['might', 'could', 'possibly', 'perhaps', 'maybe', 'seems', 'appears']
    has_hedging = any(word in response.lower() for word in hedging_words)
    
    faithfulness_score = 1.0
    
    if has_unsupported_facts:
        faithfulness_score -= 0.3
    
    if has_hedging:
        faithfulness_score += 0.1  # Hedging can be good for faithfulness
    
    # Check if response directly answers the prompt
    question_words = ['what', 'when', 'where', 'who', 'why', 'how']
    is_question = any(word in prompt.lower() for word in question_words)
    
    if is_question and not any(word in response.lower() for word in ['answer', 'response', 'information']):
        faithfulness_score += 0.1  # Direct answer is good
    
    faithfulness_score = max(0.0, min(1.0, faithfulness_score))
    
    return {
        "faithfulness_score": faithfulness_score,
        "has_unsupported_facts": has_unsupported_facts,
        "has_hedging": has_hedging,
        "is_direct_answer": is_question and any(word in response.lower() for word in ['answer', 'response', 'information']),
        "assessment": "Faithful" if faithfulness_score > 0.8 else "Mostly faithful" if faithfulness_score > 0.6 else "Somewhat faithful" if faithfulness_score > 0.4 else "Not faithful"
    }

def calculate_overall_quality_score(length_analysis, coherence_analysis, relevance_analysis, faithfulness_analysis):
    """Calculate overall quality score from all metrics."""
    weights = {
        "length": 0.2,
        "coherence": 0.25,
        "relevance": 0.3,
        "faithfulness": 0.25
    }
    
    overall_score = (
        length_analysis["length_score"] * weights["length"] +
        coherence_analysis["coherence_score"] * weights["coherence"] +
        relevance_analysis["relevance_score"] * weights["relevance"] +
        faithfulness_analysis["faithfulness_score"] * weights["faithfulness"]
    )
    
    return overall_score

def test_quality_metrics():
    """Test quality metrics with different types of prompts."""
    test_cases = [
        {
            "prompt": "What is the capital of France?",
            "description": "Simple factual question"
        },
        {
            "prompt": "Explain the benefits of renewable energy in detail.",
            "description": "Complex explanatory question"
        },
        {
            "prompt": "Write a short story about a robot learning to paint.",
            "description": "Creative task"
        }
    ]
    
    results = []
    
    print("Quality Metrics Testing")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print(f"Prompt: {test_case['prompt']}")
        print("-" * 50)
        
        try:
            response = call_openrouter_api(test_case['prompt'])
            print(f"Response: {response}")
            
            # Analyze quality metrics
            length_analysis = analyze_response_length(response)
            coherence_analysis = evaluate_coherence(response)
            relevance_analysis = evaluate_relevance(response, test_case['prompt'])
            faithfulness_analysis = evaluate_faithfulness(response, test_case['prompt'])
            overall_score = calculate_overall_quality_score(length_analysis, coherence_analysis, relevance_analysis, faithfulness_analysis)
            
            # Print detailed analysis
            print(f"\nQuality Analysis:")
            print(f"- Length: {length_analysis['word_count']} words ({length_analysis['assessment']}) - Score: {length_analysis['length_score']:.2f}")
            print(f"- Coherence: {coherence_analysis['assessment']} - Score: {coherence_analysis['coherence_score']:.2f}")
            print(f"- Relevance: {relevance_analysis['assessment']} - Score: {relevance_analysis['relevance_score']:.2f}")
            print(f"- Faithfulness: {faithfulness_analysis['assessment']} - Score: {faithfulness_analysis['faithfulness_score']:.2f}")
            print(f"- Overall Quality Score: {overall_score:.2f}")
            
            results.append({
                "test_case": test_case,
                "response": response,
                "length_analysis": length_analysis,
                "coherence_analysis": coherence_analysis,
                "relevance_analysis": relevance_analysis,
                "faithfulness_analysis": faithfulness_analysis,
                "overall_score": overall_score
            })
            
        except Exception as e:
            print(f"Error in test case {i}: {e}")
    
    return results

def generate_quality_report(results):
    """Generate a comprehensive quality report."""
    if not results:
        print("No results to analyze")
        return
    
    print("\n" + "=" * 60)
    print("QUALITY METRICS REPORT")
    print("=" * 60)
    
    # Calculate averages
    avg_length_score = sum(r['length_analysis']['length_score'] for r in results) / len(results)
    avg_coherence_score = sum(r['coherence_analysis']['coherence_score'] for r in results) / len(results)
    avg_relevance_score = sum(r['relevance_analysis']['relevance_score'] for r in results) / len(results)
    avg_faithfulness_score = sum(r['faithfulness_analysis']['faithfulness_score'] for r in results) / len(results)
    avg_overall_score = sum(r['overall_score'] for r in results) / len(results)
    
    print(f"Average Length Score: {avg_length_score:.2f}")
    print(f"Average Coherence Score: {avg_coherence_score:.2f}")
    print(f"Average Relevance Score: {avg_relevance_score:.2f}")
    print(f"Average Faithfulness Score: {avg_faithfulness_score:.2f}")
    print(f"Average Overall Quality Score: {avg_overall_score:.2f}")
    
    # Find best and worst responses
    best_response = max(results, key=lambda x: x['overall_score'])
    worst_response = min(results, key=lambda x: x['overall_score'])
    
    print(f"\nBest Response (Score: {best_response['overall_score']:.2f}):")
    print(f"- Prompt: {best_response['test_case']['prompt']}")
    print(f"- Response: {best_response['response'][:100]}...")
    
    print(f"\nWorst Response (Score: {worst_response['overall_score']:.2f}):")
    print(f"- Prompt: {worst_response['test_case']['prompt']}")
    print(f"- Response: {worst_response['response'][:100]}...")
    
    # Recommendations
    print(f"\nRecommendations:")
    if avg_overall_score > 0.8:
        print("- Excellent overall quality achieved")
    elif avg_overall_score > 0.6:
        print("- Good quality, consider minor improvements")
    else:
        print("- Quality needs improvement, review prompt design")

def main():
    """Main function to run the quality metrics exercise."""
    try:
        print("Exercise 3: Quality Metrics Implementation")
        print("Testing automated quality assessment metrics")
        print("=" * 60)
        
        # Test quality metrics
        results = test_quality_metrics()
        
        # Generate comprehensive report
        generate_quality_report(results)
        
        print("\nExercise completed successfully!")
        print("Key learning: Automated metrics can help assess response quality systematically")
        
    except Exception as e:
        print(f"Error running exercise: {e}")
        print("Please check your API key and internet connection")

if __name__ == "__main__":
    main() 