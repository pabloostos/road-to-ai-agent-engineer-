#!/usr/bin/env python3
"""
Exercise 2: Sales & Marketing Workflows

Implement business prompts for sales and marketing operations including
lead scoring, call summaries, and campaign generation.
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

def call_openrouter_api(api_key: str, prompt: str, max_tokens: int = 300) -> str:
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

def create_lead_scoring_prompt():
    """Create a prompt for lead scoring."""
    prompt = """You are a sales AI reviewing a potential customer.

Based on the description, assign a lead score from 0-100 and summarize the opportunity.
Consider factors like:
- Company size and industry
- Budget availability
- Decision-making timeline
- Technical requirements
- Strategic fit

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "lead_score": 0-100,
  "confidence": 0.0-1.0,
  "key_factors": ["factor1", "factor2"],
  "concerns": ["concern1", "concern2"],
  "next_steps": ["step1", "step2"]
}

Lead Description:
"""
    return prompt

def create_call_summary_prompt():
    """Create a prompt for summarizing sales calls."""
    prompt = """You are a sales assistant summarizing a sales call.

Create a structured summary of the conversation including:
- Key discussion points
- Customer pain points identified
- Product interest level
- Objections raised
- Next steps agreed upon
- Follow-up actions required

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "call_summary": "brief overview",
  "pain_points": ["point1", "point2"],
  "interest_level": "high|medium|low",
  "objections": ["objection1", "objection2"],
  "next_steps": ["step1", "step2"],
  "follow_up_required": true|false
}

Call Transcript:
"""
    return prompt

def create_campaign_generator_prompt():
    """Create a prompt for generating marketing campaigns."""
    prompt = """You are a marketing AI creating campaign ideas.

Based on the target audience and product information, generate campaign concepts.
Consider:
- Target audience characteristics
- Product benefits and features
- Market positioning
- Channel preferences
- Call-to-action strategies

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "campaign_name": "creative campaign title",
  "target_audience": "audience description",
  "key_message": "main value proposition",
  "channels": ["channel1", "channel2"],
  "cta": "call-to-action text",
  "success_metrics": ["metric1", "metric2"]
}

Product Information:
"""
    return prompt

def simulate_lead_scoring(lead_description: str, api_key: str = None) -> Dict[str, Any]:
    """Score leads using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_lead_scoring_prompt() + lead_description
        
        try:
            response = call_openrouter_api(api_key, prompt, max_tokens=200)
            
            # Try to extract JSON from response
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)
                    return result
                else:
                    # If no JSON found, return structured response
                    return {
                        "lead_score": 50,
                        "confidence": 0.5,
                        "key_factors": ["API response parsing issue"],
                        "concerns": ["Unable to parse response"],
                        "next_steps": ["Manual review required"]
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "lead_score": 50,
                    "confidence": 0.5,
                    "key_factors": ["JSON parsing error"],
                    "concerns": ["Response format issue"],
                    "next_steps": ["Manual review required"]
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    description_lower = lead_description.lower()
    
    # Simple scoring logic
    score = 50  # Base score
    
    # Positive factors
    if any(word in description_lower for word in ["enterprise", "large", "fortune 500"]):
        score += 20
    if any(word in description_lower for word in ["budget", "funding", "investment"]):
        score += 15
    if any(word in description_lower for word in ["urgent", "immediate", "asap"]):
        score += 10
    if any(word in description_lower for word in ["decision maker", "ceo", "cto"]):
        score += 10
    
    # Negative factors
    if any(word in description_lower for word in ["small", "startup", "limited budget"]):
        score -= 10
    if any(word in description_lower for word in ["research", "exploring", "just looking"]):
        score -= 15
    
    score = max(0, min(100, score))
    
    return {
        "lead_score": score,
        "confidence": 0.8,
        "key_factors": ["Company size", "Budget availability"] if score > 70 else ["Basic interest"],
        "concerns": ["Timeline unclear"] if score < 50 else [],
        "next_steps": ["Schedule demo", "Send proposal"] if score > 70 else ["Follow up in 30 days"]
    }

def simulate_call_summary(call_transcript: str, api_key: str = None) -> Dict[str, Any]:
    """Summarize sales calls using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_call_summary_prompt() + call_transcript
        
        try:
            response = call_openrouter_api(api_key, prompt, max_tokens=250)
            
            # Try to extract JSON from response
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)
                    return result
                else:
                    # If no JSON found, return structured response
                    return {
                        "call_summary": "API response parsing issue",
                        "pain_points": ["Unable to parse response"],
                        "interest_level": "unknown",
                        "objections": ["Response format issue"],
                        "next_steps": ["Manual review required"],
                        "follow_up_required": True
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "call_summary": "JSON parsing error",
                    "pain_points": ["Response format issue"],
                    "interest_level": "unknown",
                    "objections": ["Parsing error"],
                    "next_steps": ["Manual review required"],
                    "follow_up_required": True
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    transcript_lower = call_transcript.lower()
    
    # Extract key information
    pain_points = []
    if any(word in transcript_lower for word in ["slow", "inefficient", "problem"]):
        pain_points.append("Process inefficiency")
    if any(word in transcript_lower for word in ["cost", "expensive", "budget"]):
        pain_points.append("Cost concerns")
    
    interest_level = "medium"
    if any(word in transcript_lower for word in ["interested", "excited", "perfect"]):
        interest_level = "high"
    elif any(word in transcript_lower for word in ["not sure", "maybe", "later"]):
        interest_level = "low"
    
    return {
        "call_summary": "Productive discussion about business needs and solution fit",
        "pain_points": pain_points,
        "interest_level": interest_level,
        "objections": ["Timeline concerns"] if interest_level == "medium" else [],
        "next_steps": ["Send proposal", "Schedule follow-up"],
        "follow_up_required": True
    }

def simulate_campaign_generation(product_info: str, api_key: str = None) -> Dict[str, Any]:
    """Generate marketing campaigns using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_campaign_generator_prompt() + product_info
        
        try:
            response = call_openrouter_api(api_key, prompt, max_tokens=300)
            
            # Try to extract JSON from response
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)
                    return result
                else:
                    # If no JSON found, return structured response
                    return {
                        "campaign_name": "API Response Campaign",
                        "target_audience": "Unable to parse response",
                        "key_message": "API response parsing issue",
                        "channels": ["Manual review required"],
                        "cta": "Contact support",
                        "success_metrics": ["Response parsing"]
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "campaign_name": "JSON Error Campaign",
                    "target_audience": "Response format issue",
                    "key_message": "JSON parsing error",
                    "channels": ["Manual review required"],
                    "cta": "Contact support",
                    "success_metrics": ["Parsing error"]
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    info_lower = product_info.lower()
    
    if "ai" in info_lower or "automation" in info_lower:
        campaign_name = "AI-Powered Efficiency Revolution"
        key_message = "Transform your business with intelligent automation"
    elif "cloud" in info_lower or "saas" in info_lower:
        campaign_name = "Cloud-First Future"
        key_message = "Scale your business with cloud-native solutions"
    else:
        campaign_name = "Business Transformation Campaign"
        key_message = "Unlock your business potential"
    
    return {
        "campaign_name": campaign_name,
        "target_audience": "Mid-market companies seeking digital transformation",
        "key_message": key_message,
        "channels": ["LinkedIn", "Email", "Webinars"],
        "cta": "Schedule your free consultation today",
        "success_metrics": ["Lead generation", "Demo bookings", "Conversion rate"]
    }

def run_sales_marketing_tests():
    """Run sales and marketing workflow tests."""
    test_cases = [
        {
            "name": "Enterprise Lead",
            "description": "Fortune 500 logistics company looking for AI-powered route optimization. Budget: $500k, timeline: 3 months, decision maker: CTO",
            "type": "lead_scoring"
        },
        {
            "name": "Startup Lead",
            "description": "Small startup exploring automation tools. Limited budget, still in research phase",
            "type": "lead_scoring"
        },
        {
            "name": "Sales Call Summary",
            "description": "Discussed current pain points with manual processes. Customer showed interest in automation features. Concerns about implementation timeline.",
            "type": "call_summary"
        },
        {
            "name": "Campaign Generation",
            "description": "AI-powered business automation platform. Target: Mid-market companies struggling with manual processes",
            "type": "campaign_generation"
        }
    ]
    return test_cases

def main():
    """Main function for Exercise 2."""
    print("Exercise 2: Sales & Marketing Workflows")
    print("=" * 45)
    
    # Load API key
    api_key = load_api_key()
    
    # Define prompts
    lead_scoring_prompt = create_lead_scoring_prompt()
    call_summary_prompt = create_call_summary_prompt()
    campaign_prompt = create_campaign_generator_prompt()
    
    print("Business Prompts Created:")
    print("1. Lead Scoring System")
    print("2. Call Summary Generator")
    print("3. Campaign Generator")
    print()
    
    # Run test cases
    test_cases = run_sales_marketing_tests()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print("-" * 40)
        print(f"Input: {test_case['description']}")
        print()
        
        if test_case['type'] == 'lead_scoring':
            result = simulate_lead_scoring(test_case['description'], api_key)
            print("Lead Scoring Result:")
            print(json.dumps(result, indent=2))
            
        elif test_case['type'] == 'call_summary':
            result = simulate_call_summary(test_case['description'], api_key)
            print("Call Summary Result:")
            print(json.dumps(result, indent=2))
            
        elif test_case['type'] == 'campaign_generation':
            result = simulate_campaign_generation(test_case['description'], api_key)
            print("Campaign Generation Result:")
            print(json.dumps(result, indent=2))
        
        print()

if __name__ == "__main__":
    main() 