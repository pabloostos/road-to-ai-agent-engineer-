"""
Exercise 4: Comprehensive Evaluation Framework
Build a complete evaluation system that combines multiple assessment methods.
"""

import os
import requests
import json
import statistics
import time
from datetime import datetime
from dotenv import load_dotenv

def load_api_key():
    """Load OpenRouter API key from environment variables."""
    load_dotenv()
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    return api_key

def call_openrouter_api(prompt, temperature=0.1, model="openai/gpt-3.5-turbo", max_tokens=200):
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
        "max_tokens": max_tokens
    }
    
    start_time = time.time()
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    end_time = time.time()
    
    if response.status_code == 200:
        result = response.json()
        return {
            "content": result['choices'][0]['message']['content'],
            "response_time": end_time - start_time,
            "tokens_used": result.get('usage', {}).get('total_tokens', 0)
        }
    else:
        raise Exception(f"API Error: {response.status_code}")

class ComprehensiveEvaluator:
    """Comprehensive evaluation framework for LLM responses."""
    
    def __init__(self, config=None):
        """Initialize the evaluator with configuration."""
        self.config = config or {
            "default_model": "openai/gpt-3.5-turbo",
            "default_temperature": 0.1,
            "consistency_tests": 3,
            "similarity_threshold": 0.5,
            "quality_weights": {
                "length": 0.2,
                "coherence": 0.25,
                "relevance": 0.3,
                "faithfulness": 0.25
            }
        }
        self.results = []
    
    def test_consistency(self, prompt, num_tests=None, temperature=None):
        """Test response consistency across multiple calls."""
        num_tests = num_tests or self.config["consistency_tests"]
        temperature = temperature or self.config["default_temperature"]
        
        responses = []
        response_times = []
        
        print(f"Testing consistency: {num_tests} calls with temperature={temperature}")
        
        for i in range(num_tests):
            try:
                result = call_openrouter_api(prompt, temperature)
                responses.append(result["content"])
                response_times.append(result["response_time"])
                print(f"  Call {i+1}: {result['content'][:50]}... (Time: {result['response_time']:.2f}s)")
            except Exception as e:
                print(f"  Error in call {i+1}: {e}")
        
        # Calculate consistency metrics
        unique_responses = set(responses)
        consistency_percentage = ((len(responses) - len(unique_responses)) / len(responses)) * 100 if responses else 0
        
        return {
            "responses": responses,
            "consistency_percentage": consistency_percentage,
            "variations": len(unique_responses),
            "avg_response_time": statistics.mean(response_times) if response_times else 0,
            "total_responses": len(responses)
        }
    
    def test_semantic_similarity(self, prompts):
        """Test semantic similarity across similar prompts."""
        print(f"Testing semantic similarity across {len(prompts)} prompts")
        
        responses = {}
        similarity_scores = []
        
        # Get responses for all prompts
        for i, prompt in enumerate(prompts):
            try:
                result = call_openrouter_api(prompt)
                responses[prompt] = result["content"]
                print(f"  Prompt {i+1}: {prompt}")
                print(f"  Response: {result['content'][:50]}...")
            except Exception as e:
                print(f"  Error with prompt {i+1}: {e}")
                responses[prompt] = "Error"
        
        # Calculate similarity between all pairs
        prompt_list = list(responses.keys())
        for i in range(len(prompt_list)):
            for j in range(i + 1, len(prompt_list)):
                similarity = self._calculate_similarity(responses[prompt_list[i]], responses[prompt_list[j]])
                similarity_scores.append(similarity)
                print(f"  Similarity {i+1}-{j+1}: {similarity:.2f}")
        
        avg_similarity = statistics.mean(similarity_scores) if similarity_scores else 0
        
        return {
            "responses": responses,
            "similarity_scores": similarity_scores,
            "average_similarity": avg_similarity,
            "total_comparisons": len(similarity_scores)
        }
    
    def _calculate_similarity(self, response1, response2):
        """Calculate simple similarity between two responses."""
        words1 = set(response1.lower().split())
        words2 = set(response2.lower().split())
        
        if not words1 or not words2:
            return 0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0
    
    def evaluate_quality_metrics(self, response, prompt):
        """Evaluate comprehensive quality metrics."""
        # Length analysis
        word_count = len(response.split())
        length_score = 1.0 if 20 <= word_count <= 100 else 0.7 if 10 <= word_count <= 150 else 0.3
        
        # Coherence analysis (simplified)
        sentences = response.split('.')
        coherence_score = 1.0 if len(sentences) > 1 else 0.8
        
        # Relevance analysis (simplified)
        prompt_words = set(prompt.lower().split())
        response_words = set(response.lower().split())
        common_words = prompt_words.intersection(response_words)
        relevance_score = len(common_words) / len(prompt_words) if prompt_words else 0.5
        
        # Faithfulness analysis (simplified)
        faithfulness_score = 1.0  # Assume faithful for simplicity
        
        # Calculate overall score
        weights = self.config["quality_weights"]
        overall_score = (
            length_score * weights["length"] +
            coherence_score * weights["coherence"] +
            relevance_score * weights["relevance"] +
            faithfulness_score * weights["faithfulness"]
        )
        
        return {
            "length_score": length_score,
            "coherence_score": coherence_score,
            "relevance_score": relevance_score,
            "faithfulness_score": faithfulness_score,
            "overall_score": overall_score,
            "word_count": word_count
        }
    
    def run_comprehensive_evaluation(self, test_cases):
        """Run comprehensive evaluation on multiple test cases."""
        print("Comprehensive Evaluation Framework")
        print("=" * 60)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest Case {i}: {test_case['description']}")
            print(f"Prompt: {test_case['prompt']}")
            print("-" * 50)
            
            # Get initial response
            try:
                result = call_openrouter_api(test_case['prompt'])
                response = result["content"]
                print(f"Response: {response}")
                
                # Test consistency
                consistency_results = self.test_consistency(test_case['prompt'])
                
                # Evaluate quality metrics
                quality_results = self.evaluate_quality_metrics(response, test_case['prompt'])
                
                # Store comprehensive results
                case_results = {
                    "test_case": test_case,
                    "response": response,
                    "consistency": consistency_results,
                    "quality": quality_results,
                    "performance": {
                        "response_time": result["response_time"],
                        "tokens_used": result["tokens_used"]
                    }
                }
                
                self.results.append(case_results)
                
                # Print summary for this case
                print(f"\nCase {i} Summary:")
                print(f"- Consistency: {consistency_results['consistency_percentage']:.1f}%")
                print(f"- Quality Score: {quality_results['overall_score']:.2f}")
                print(f"- Response Time: {result['response_time']:.2f}s")
                print(f"- Tokens Used: {result['tokens_used']}")
                
            except Exception as e:
                print(f"Error in test case {i}: {e}")
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive evaluation report."""
        if not self.results:
            print("No results to analyze")
            return
        
        print("\n" + "=" * 60)
        print("COMPREHENSIVE EVALUATION REPORT")
        print("=" * 60)
        
        # Calculate overall statistics
        total_cases = len(self.results)
        avg_consistency = statistics.mean([r['consistency']['consistency_percentage'] for r in self.results])
        avg_quality = statistics.mean([r['quality']['overall_score'] for r in self.results])
        avg_response_time = statistics.mean([r['performance']['response_time'] for r in self.results])
        total_tokens = sum([r['performance']['tokens_used'] for r in self.results])
        
        print(f"Total Test Cases: {total_cases}")
        print(f"Average Consistency: {avg_consistency:.1f}%")
        print(f"Average Quality Score: {avg_quality:.2f}")
        print(f"Average Response Time: {avg_response_time:.2f}s")
        print(f"Total Tokens Used: {total_tokens}")
        
        # Find best and worst cases
        best_case = max(self.results, key=lambda x: x['quality']['overall_score'])
        worst_case = min(self.results, key=lambda x: x['quality']['overall_score'])
        
        print(f"\nBest Performing Case:")
        print(f"- Description: {best_case['test_case']['description']}")
        print(f"- Quality Score: {best_case['quality']['overall_score']:.2f}")
        print(f"- Consistency: {best_case['consistency']['consistency_percentage']:.1f}%")
        
        print(f"\nWorst Performing Case:")
        print(f"- Description: {worst_case['test_case']['description']}")
        print(f"- Quality Score: {worst_case['quality']['overall_score']:.2f}")
        print(f"- Consistency: {worst_case['consistency']['consistency_percentage']:.1f}%")
        
        # Recommendations
        print(f"\nRecommendations:")
        if avg_quality > 0.8:
            print("- Excellent overall quality achieved")
        elif avg_quality > 0.6:
            print("- Good quality, consider minor optimizations")
        else:
            print("- Quality needs improvement, review prompt design")
        
        if avg_consistency > 80:
            print("- High consistency achieved")
        elif avg_consistency > 50:
            print("- Moderate consistency, consider temperature adjustments")
        else:
            print("- Low consistency, review model parameters")
        
        # Save results to file
        self._save_results()
    
    def _save_results(self):
        """Save evaluation results to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_results_{timestamp}.json"
        
        # Prepare data for JSON serialization
        serializable_results = []
        for result in self.results:
            serializable_result = {
                "test_case": result["test_case"],
                "response": result["response"],
                "consistency": result["consistency"],
                "quality": result["quality"],
                "performance": result["performance"]
            }
            serializable_results.append(serializable_result)
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"\nResults saved to: {filename}")

def main():
    """Main function to run the comprehensive evaluation framework."""
    try:
        print("Exercise 4: Comprehensive Evaluation Framework")
        print("Testing complete evaluation system with multiple metrics")
        print("=" * 60)
        
        # Define test cases
        test_cases = [
            {
                "prompt": "What is the capital of France and what is something interesting about it?",
                "description": "Simple factual question with detail request"
            },
            {
                "prompt": "Explain the benefits of renewable energy in detail.",
                "description": "Complex explanatory question"
            },
            {
                "prompt": "Write a short story about a robot learning to paint.",
                "description": "Creative narrative task"
            },
            {
                "prompt": "Compare and contrast traditional education vs online learning.",
                "description": "Analytical comparison task"
            }
        ]
        
        # Initialize evaluator
        evaluator = ComprehensiveEvaluator()
        
        # Run comprehensive evaluation
        evaluator.run_comprehensive_evaluation(test_cases)
        
        # Generate comprehensive report
        evaluator.generate_comprehensive_report()
        
        print("\nExercise completed successfully!")
        print("Key learning: Comprehensive evaluation provides holistic view of model performance")
        
    except Exception as e:
        print(f"Error running exercise: {e}")
        print("Please check your API key and internet connection")

if __name__ == "__main__":
    main() 