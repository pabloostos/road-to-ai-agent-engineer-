#!/usr/bin/env python3
"""
Exercise 1: Customer Support Automation

Implement business prompts for customer support workflows including
ticket classification, reply drafting, and sentiment analysis.
"""

import json
import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, List

def load_api_key():
    """Load OpenRouter API key from environment variables."""
    load_dotenv()
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("Warning: OPENROUTER_API_KEY not found!")
        print("This exercise will use simulated responses for demonstration.")
        return None
    
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
            return f"API Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error: {e}"

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

def simulate_ticket_classification(ticket_text: str, api_key: str = None) -> Dict[str, Any]:
    """Classify support tickets using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_support_ticket_classifier_prompt() + ticket_text
        
        try:
            response = call_openrouter_api(api_key, prompt, max_tokens=150)
            
            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)
                    return result
                else:
                    # If no JSON found, return structured response
                    return {
                        "category": "Technical",  # Default fallback
                        "severity": 3,
                        "urgency_reason": "API response parsing issue"
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "category": "Other",
                    "severity": 2,
                    "urgency_reason": "Unable to parse API response"
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    ticket_lower = ticket_text.lower()
    
    if any(word in ticket_lower for word in ["billing", "charge", "payment", "invoice", "cost"]):
        category = "Billing"
        severity = 4
        urgency_reason = "Financial impact on customer"
    elif any(word in ticket_lower for word in ["technical", "bug", "error", "broken", "not working"]):
        category = "Technical"
        severity = 3
        urgency_reason = "Service functionality affected"
    elif any(word in ticket_lower for word in ["account", "login", "password", "access"]):
        category = "Account"
        severity = 2
        urgency_reason = "Access issues"
    else:
        category = "Other"
        severity = 1
        urgency_reason = "General inquiry"
    
    return {
        "category": category,
        "severity": severity,
        "urgency_reason": urgency_reason
    }

def simulate_reply_drafting(ticket_text: str, api_key: str = None) -> str:
    """Draft customer support replies using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_reply_drafter_prompt() + ticket_text
        
        try:
            response = call_openrouter_api(api_key, prompt, max_tokens=300)
            return response
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    ticket_lower = ticket_text.lower()
    
    if "billing" in ticket_lower or "charge" in ticket_lower:
        reply = """Dear Customer,

Thank you for reaching out to us regarding your billing concern. I understand this can be frustrating, and I'm here to help resolve this issue.

I can see that you've been charged twice this month. Let me investigate this immediately and get back to you within 24 hours with a resolution.

In the meantime, I've put a temporary hold on any additional charges to your account to prevent further issues.

If you need immediate assistance, you can also reach our billing team directly at 1-800-SUPPORT.

Best regards,
Customer Support Team"""
    
    elif "technical" in ticket_lower or "error" in ticket_lower:
        reply = """Dear Customer,

Thank you for reporting this technical issue. I understand how important it is to have our services working properly for you.

I've logged your issue and our technical team will investigate this immediately. You should receive an update within 2-4 hours.

To help us resolve this faster, could you please provide:
- Screenshots of any error messages
- Steps to reproduce the issue
- Browser/device information

We appreciate your patience as we work to get this resolved for you.

Best regards,
Technical Support Team"""
    
    else:
        reply = """Dear Customer,

Thank you for contacting our support team. I've received your inquiry and I'm here to help.

I'm currently reviewing your request and will provide you with a detailed response within the next business day.

If this is urgent, please let us know and we'll prioritize your case accordingly.

Thank you for your patience.

Best regards,
Customer Support Team"""
    
    return reply

def simulate_sentiment_analysis(customer_message: str, api_key: str = None) -> Dict[str, Any]:
    """Analyze customer sentiment using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_sentiment_analyzer_prompt() + customer_message
        
        try:
            response = call_openrouter_api(api_key, prompt, max_tokens=150)
            
            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)
                    return result
                else:
                    # If no JSON found, return structured response
                    return {
                        "sentiment": "neutral",
                        "confidence": 0.5,
                        "key_emotions": ["unknown"],
                        "escalation_needed": False
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "sentiment": "neutral",
                    "confidence": 0.5,
                    "key_emotions": ["parsing_error"],
                    "escalation_needed": False
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    message_lower = customer_message.lower()
    
    # Simple sentiment analysis based on keywords
    negative_words = ["angry", "frustrated", "terrible", "horrible", "hate", "disappointed"]
    positive_words = ["happy", "great", "excellent", "love", "amazing", "thank you"]
    
    negative_count = sum(1 for word in negative_words if word in message_lower)
    positive_count = sum(1 for word in positive_words if word in message_lower)
    
    if negative_count > positive_count:
        sentiment = "negative"
        confidence = 0.8
        key_emotions = ["frustration", "anger"]
        escalation_needed = True
    elif positive_count > negative_count:
        sentiment = "positive"
        confidence = 0.7
        key_emotions = ["satisfaction", "gratitude"]
        escalation_needed = False
    else:
        sentiment = "neutral"
        confidence = 0.6
        key_emotions = ["neutral"]
        escalation_needed = False
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "key_emotions": key_emotions,
        "escalation_needed": escalation_needed
    }

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
        }
    ]
    return test_cases

def main():
    """Main function for Exercise 1."""
    print("Exercise 1: Customer Support Automation")
    print("=" * 45)
    
    # Load API key
    api_key = load_api_key()
    
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
        print("-" * 40)
        print(f"Ticket: {test_case['ticket']}")
        print()
        
        if test_case['type'] == 'classification':
            # Classify ticket
            classification = simulate_ticket_classification(test_case['ticket'], api_key)
            print("Classification Result:")
            print(json.dumps(classification, indent=2))
            print()
            
            # Draft reply
            reply = simulate_reply_drafting(test_case['ticket'], api_key)
            print("Drafted Reply:")
            print(reply)
            print()
            
        elif test_case['type'] == 'sentiment':
            # Analyze sentiment
            sentiment = simulate_sentiment_analysis(test_case['ticket'], api_key)
            print("Sentiment Analysis:")
            print(json.dumps(sentiment, indent=2))
            print()
        
        print()

if __name__ == "__main__":
    main() 