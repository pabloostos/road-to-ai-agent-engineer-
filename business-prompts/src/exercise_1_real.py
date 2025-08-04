#!/usr/bin/env python3
"""
Exercise 1: Customer Support Automation (Real API Only)

Implement business prompts for customer support workflows using only OpenRouter API.
No simulation fallbacks - pure API-driven responses.
"""

import json
import os
import requests
import re
from dotenv import load_dotenv
from typing import Dict, Any, List

def load_api_key():
    """Load OpenRouter API key from environment variables."""
    load_dotenv()
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables!")
    
    return api_key

def call_openrouter_api(api_key: str, prompt: str, max_tokens: int = 200) -> str:
    """Call OpenRouter API with the given prompt."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.1
    }
    
    try:
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
            raise Exception(f"API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        raise Exception(f"API call failed: {e}")

def create_support_ticket_classifier_prompt():
    """Create a prompt for classifying support tickets."""
    prompt = """You are an AI assistant for a customer support team.

Analyze the following support ticket and classify it into one of these categories: ["Billing", "Technical", "Account", "Other"].

Also assign a severity score from 1 (low) to 5 (critical) and provide a brief urgency reason.

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "category": "Billing|Technical|Account|Other",
  "severity": 1-5,
  "urgency_reason": "brief explanation"
}

Support Ticket:
"""
    return prompt

def create_reply_drafter_prompt():
    """Create a prompt for drafting customer support replies."""
    prompt = """You are a professional customer support representative.

Based on the following support ticket, draft a helpful and professional reply that:
1. Acknowledges the customer's issue
2. Provides a clear explanation or solution
3. Includes next steps if needed
4. Uses a professional and empathetic tone

Write a complete email reply that the customer support team can send directly to the customer.

Support Ticket:
"""
    return prompt

def create_sentiment_analyzer_prompt():
    """Create a prompt for analyzing customer sentiment."""
    prompt = """You are an AI analyzing customer sentiment from support interactions.

Analyze the following customer message and determine the sentiment and emotional state.

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "sentiment": "positive|negative|neutral|mixed",
  "confidence": 0.0-1.0,
  "key_emotions": ["emotion1", "emotion2"],
  "escalation_needed": true|false
}

Customer Message:
"""
    return prompt

def classify_ticket(ticket_text: str, api_key: str) -> Dict[str, Any]:
    """Classify support tickets using OpenRouter API."""
    prompt = create_support_ticket_classifier_prompt() + ticket_text
    
    response = call_openrouter_api(api_key, prompt, max_tokens=150)
    
    # Extract JSON from response
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        result = json.loads(json_str)
        return result
    else:
        raise Exception("Could not extract JSON from API response")

def draft_reply(ticket_text: str, api_key: str) -> str:
    """Draft customer support replies using OpenRouter API."""
    prompt = create_reply_drafter_prompt() + ticket_text
    
    response = call_openrouter_api(api_key, prompt, max_tokens=400)
    return response

def analyze_sentiment(customer_message: str, api_key: str) -> Dict[str, Any]:
    """Analyze customer sentiment using OpenRouter API."""
    prompt = create_sentiment_analyzer_prompt() + customer_message
    
    response = call_openrouter_api(api_key, prompt, max_tokens=150)
    
    # Extract JSON from response
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        result = json.loads(json_str)
        return result
    else:
        raise Exception("Could not extract JSON from API response")

def run_customer_support_tests():
    """Run customer support automation tests."""
    test_cases = [
        {
            "name": "Billing Issue",
            "ticket": "I was charged twice this month and I can't reach anyone on the phone! This is unacceptable.",
            "type": "classification"
        },
        {
            "name": "Technical Problem", 
            "ticket": "The app keeps crashing when I try to upload files. I've tried everything but it's still broken.",
            "type": "classification"
        },
        {
            "name": "Account Access",
            "ticket": "I can't log into my account. It says my password is wrong but I'm sure it's correct.",
            "type": "classification"
        },
        {
            "name": "Positive Feedback",
            "ticket": "Thank you so much! The new feature is amazing and works perfectly. You guys are the best!",
            "type": "sentiment"
        },
        {
            "name": "Negative Complaint",
            "ticket": "This is the worst service I've ever experienced. I'm extremely angry and frustrated with your company!",
            "type": "sentiment"
        }
    ]
    return test_cases

def main():
    """Main function for Exercise 1 (Real API Only)."""
    print("Exercise 1: Customer Support Automation (Real API Only)")
    print("=" * 60)
    
    try:
        # Load API key
        api_key = load_api_key()
        print("✅ OpenRouter API key loaded successfully")
        print()
        
        # Define prompts
        classifier_prompt = create_support_ticket_classifier_prompt()
        reply_prompt = create_reply_drafter_prompt()
        sentiment_prompt = create_sentiment_analyzer_prompt()
        
        print("Business Prompts Created:")
        print("1. Support Ticket Classifier")
        print("2. Reply Drafter") 
        print("3. Sentiment Analyzer")
        print()
        
        # Run test cases
        test_cases = run_customer_support_tests()
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test Case {i}: {test_case['name']}")
            print("-" * 50)
            print(f"Ticket: {test_case['ticket']}")
            print()
            
            try:
                if test_case['type'] == 'classification':
                    # Classify ticket
                    classification = classify_ticket(test_case['ticket'], api_key)
                    print("Classification Result:")
                    print(json.dumps(classification, indent=2))
                    print()
                    
                    # Draft reply
                    reply = draft_reply(test_case['ticket'], api_key)
                    print("Drafted Reply:")
                    print(reply)
                    print()
                    
                elif test_case['type'] == 'sentiment':
                    # Analyze sentiment
                    sentiment = analyze_sentiment(test_case['ticket'], api_key)
                    print("Sentiment Analysis:")
                    print(json.dumps(sentiment, indent=2))
                    print()
                
                print("✅ Test case completed successfully")
                print()
                
            except Exception as e:
                print(f"❌ Error in test case {i}: {e}")
                print()
        
        print("🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main() 