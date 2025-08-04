#!/usr/bin/env python3
"""
Exercise 4: Cross-Domain Integration

Implement prompts that integrate across multiple business domains
to create comprehensive workflow automation.
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

def call_openrouter_api(api_key: str, prompt: str, max_tokens: int = 500) -> str:
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

def create_customer_journey_prompt():
    """Create a prompt for analyzing customer journey across departments."""
    prompt = """You are a business analyst analyzing customer interactions across multiple departments.

Create a comprehensive customer journey analysis that integrates data from:
- Customer Support (tickets, sentiment)
- Sales (lead scoring, call summaries)
- Marketing (campaign responses)
- Operations (incident impact)

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "customer_id": "unique identifier",
  "journey_stage": "awareness|consideration|purchase|retention|advocacy",
  "department_touchpoints": [{"department": "dept", "interaction": "description"}],
  "overall_sentiment": "positive|negative|neutral",
  "risk_score": 0-100,
  "opportunity_score": 0-100,
  "recommended_actions": ["action1", "action2"],
  "escalation_needed": true|false
}

Customer Data:
"""
    return prompt

def create_workflow_orchestrator_prompt():
    """Create a prompt for orchestrating multi-department workflows."""
    prompt = """You are a workflow orchestrator managing business processes across departments.

Based on the input, determine the optimal workflow sequence and assign tasks to appropriate departments.
Consider:
- Process priority and urgency
- Department capabilities and availability
- SLA requirements
- Resource allocation
- Handoff points

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "workflow_id": "unique identifier",
  "priority": "low|medium|high|critical",
  "departments_involved": ["dept1", "dept2"],
  "task_sequence": ["task1", "task2"],
  "estimated_duration": "time estimate",
  "dependencies": ["dep1", "dep2"],
  "success_metrics": ["metric1", "metric2"],
  "escalation_triggers": ["trigger1", "trigger2"]
}

Workflow Request:
"""
    return prompt

def create_business_intelligence_prompt():
    """Create a prompt for generating business intelligence reports."""
    prompt = """You are a business intelligence analyst creating comprehensive reports.

Synthesize data from multiple departments to provide actionable insights.
Include:
- Key performance indicators
- Trend analysis
- Cross-department correlations
- Risk assessments
- Opportunity identification
- Strategic recommendations

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "report_period": "time period",
  "executive_summary": "high-level insights",
  "department_performance": {"dept": "performance"},
  "trends": ["trend1", "trend2"],
  "risks": ["risk1", "risk2"],
  "opportunities": ["opp1", "opp2"],
  "recommendations": ["rec1", "rec2"],
  "next_period_focus": ["focus1", "focus2"]
}

Business Data:
"""
    return prompt

def simulate_customer_journey_analysis(customer_data: str, api_key: str = None) -> Dict[str, Any]:
    """Analyze customer journey using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_customer_journey_prompt() + customer_data
        
        try:
            response = call_openrouter_api(api_key, prompt, max_tokens=400)
            
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
                        "customer_id": "CUST-ERROR",
                        "journey_stage": "unknown",
                        "department_touchpoints": [{"department": "API", "interaction": "Response parsing issue"}],
                        "overall_sentiment": "neutral",
                        "risk_score": 50,
                        "opportunity_score": 50,
                        "recommended_actions": ["Manual review required"],
                        "escalation_needed": True
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "customer_id": "CUST-ERROR",
                    "journey_stage": "unknown",
                    "department_touchpoints": [{"department": "API", "interaction": "JSON parsing error"}],
                    "overall_sentiment": "neutral",
                    "risk_score": 50,
                    "opportunity_score": 50,
                    "recommended_actions": ["Manual review required"],
                    "escalation_needed": True
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    data_lower = customer_data.lower()
    
    # Determine journey stage
    if any(word in data_lower for word in ["new", "first", "discovered"]):
        journey_stage = "awareness"
        risk_score = 70
        opportunity_score = 30
    elif any(word in data_lower for word in ["interested", "evaluating", "comparing"]):
        journey_stage = "consideration"
        risk_score = 50
        opportunity_score = 60
    elif any(word in data_lower for word in ["purchased", "bought", "signed"]):
        journey_stage = "purchase"
        risk_score = 30
        opportunity_score = 80
    else:
        journey_stage = "retention"
        risk_score = 20
        opportunity_score = 90
    
    # Determine sentiment
    if any(word in data_lower for word in ["happy", "satisfied", "great"]):
        overall_sentiment = "positive"
    elif any(word in data_lower for word in ["unhappy", "frustrated", "angry"]):
        overall_sentiment = "negative"
    else:
        overall_sentiment = "neutral"
    
    return {
        "customer_id": "CUST-12345",
        "journey_stage": journey_stage,
        "department_touchpoints": [
            {"department": "Marketing", "interaction": "Campaign email opened"},
            {"department": "Sales", "interaction": "Demo scheduled"},
            {"department": "Support", "interaction": "Initial setup call"}
        ],
        "overall_sentiment": overall_sentiment,
        "risk_score": risk_score,
        "opportunity_score": opportunity_score,
        "recommended_actions": [
            "Sales: Follow up with personalized offer",
            "Support: Proactive check-in call",
            "Marketing: Send relevant case studies"
        ],
        "escalation_needed": risk_score > 60
    }

def simulate_workflow_orchestration(workflow_request: str, api_key: str = None) -> Dict[str, Any]:
    """Orchestrate workflows using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_workflow_orchestrator_prompt() + workflow_request
        
        try:
            response = call_openrouter_api(api_key, prompt, max_tokens=400)
            
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
                        "workflow_id": "WF-ERROR",
                        "priority": "medium",
                        "departments_involved": ["API response parsing issue"],
                        "task_sequence": ["Manual review required"],
                        "estimated_duration": "unknown",
                        "dependencies": ["Response format issue"],
                        "success_metrics": ["Manual review"],
                        "escalation_triggers": ["API parsing error"]
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "workflow_id": "WF-ERROR",
                    "priority": "medium",
                    "departments_involved": ["JSON parsing error"],
                    "task_sequence": ["Manual review required"],
                    "estimated_duration": "unknown",
                    "dependencies": ["Parsing error"],
                    "success_metrics": ["Manual review"],
                    "escalation_triggers": ["JSON parsing error"]
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    request_lower = workflow_request.lower()
    
    # Determine priority
    if any(word in request_lower for word in ["urgent", "critical", "emergency"]):
        priority = "critical"
        estimated_duration = "2-4 hours"
    elif any(word in request_lower for word in ["important", "high", "priority"]):
        priority = "high"
        estimated_duration = "1-2 days"
    else:
        priority = "medium"
        estimated_duration = "3-5 days"
    
    # Determine departments involved
    departments = []
    if any(word in request_lower for word in ["support", "customer", "issue"]):
        departments.append("Customer Support")
    if any(word in request_lower for word in ["sales", "lead", "opportunity"]):
        departments.append("Sales")
    if any(word in request_lower for word in ["technical", "system", "bug"]):
        departments.append("Engineering")
    if any(word in request_lower for word in ["marketing", "campaign", "promotion"]):
        departments.append("Marketing")
    
    return {
        "workflow_id": "WF-2024-001",
        "priority": priority,
        "departments_involved": departments,
        "task_sequence": [
            "Initial assessment",
            "Department handoff",
            "Task execution",
            "Quality review",
            "Customer notification"
        ],
        "estimated_duration": estimated_duration,
        "dependencies": ["Approval required", "Resource allocation"],
        "success_metrics": ["Resolution time", "Customer satisfaction", "Cost efficiency"],
        "escalation_triggers": ["SLA breach", "Customer complaint", "Technical complexity"]
    }

def simulate_business_intelligence_report(business_data: str, api_key: str = None) -> Dict[str, Any]:
    """Generate business intelligence reports using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_business_intelligence_prompt() + business_data
        
        try:
            response = call_openrouter_api(api_key, prompt, max_tokens=500)
            
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
                        "report_period": "Q1 2024",
                        "executive_summary": "API response parsing issue. Manual review required.",
                        "department_performance": {
                            "API": "Response parsing issue",
                            "Manual": "Review required"
                        },
                        "trends": ["API parsing error"],
                        "risks": ["Response format issue"],
                        "opportunities": ["Manual review"],
                        "recommendations": ["Contact technical team"],
                        "next_period_focus": ["API integration"]
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "report_period": "Q1 2024",
                    "executive_summary": "JSON parsing error. Manual review required.",
                    "department_performance": {
                        "API": "JSON parsing error",
                        "Manual": "Review required"
                    },
                    "trends": ["JSON parsing error"],
                    "risks": ["Parsing error"],
                    "opportunities": ["Manual review"],
                    "recommendations": ["Contact technical team"],
                    "next_period_focus": ["API integration"]
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    data_lower = business_data.lower()
    
    # Generate insights based on data
    if "growth" in data_lower or "increase" in data_lower:
        trends = ["Revenue growth", "Customer acquisition", "Market expansion"]
        opportunities = ["Upsell existing customers", "Enter new markets", "Product development"]
    elif "decline" in data_lower or "decrease" in data_lower:
        trends = ["Revenue decline", "Customer churn", "Market contraction"]
        opportunities = ["Customer retention programs", "Cost optimization", "Product improvements"]
    else:
        trends = ["Stable performance", "Consistent metrics", "Market stability"]
        opportunities = ["Process optimization", "Efficiency improvements", "Innovation initiatives"]
    
    return {
        "report_period": "Q1 2024",
        "executive_summary": "Business performance shows mixed results with opportunities for improvement",
        "department_performance": {
            "Sales": "Meeting targets",
            "Support": "Above average satisfaction",
            "Marketing": "Campaign effectiveness improving",
            "Operations": "Efficiency gains achieved"
        },
        "trends": trends,
        "risks": ["Market competition", "Economic uncertainty", "Technology disruption"],
        "opportunities": opportunities,
        "recommendations": [
            "Invest in customer retention",
            "Optimize operational efficiency",
            "Enhance product offerings"
        ],
        "next_period_focus": ["Customer success", "Revenue growth", "Operational excellence"]
    }

def run_cross_domain_tests():
    """Run cross-domain integration tests."""
    test_cases = [
        {
            "name": "Customer Journey Analysis",
            "description": "New customer who discovered us through marketing campaign, attended sales demo, and has initial support setup. Shows interest in premium features.",
            "type": "customer_journey"
        },
        {
            "name": "Workflow Orchestration",
            "description": "Urgent customer issue requiring technical investigation, sales follow-up, and marketing communication. High-priority enterprise customer.",
            "type": "workflow_orchestration"
        },
        {
            "name": "Business Intelligence Report",
            "description": "Q1 performance data showing 15% revenue growth, 8% customer churn, improved support satisfaction, and successful marketing campaigns.",
            "type": "business_intelligence"
        }
    ]
    return test_cases

def main():
    """Main function for Exercise 4."""
    print("Exercise 4: Cross-Domain Integration")
    print("=" * 40)
    
    # Load API key
    api_key = load_api_key()
    
    # Define prompts
    journey_prompt = create_customer_journey_prompt()
    workflow_prompt = create_workflow_orchestrator_prompt()
    bi_prompt = create_business_intelligence_prompt()
    
    print("Business Prompts Created:")
    print("1. Customer Journey Analyzer")
    print("2. Workflow Orchestrator")
    print("3. Business Intelligence Reporter")
    print()
    
    # Run test cases
    test_cases = run_cross_domain_tests()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print("-" * 40)
        print(f"Input: {test_case['description']}")
        print()
        
        if test_case['type'] == 'customer_journey':
            result = simulate_customer_journey_analysis(test_case['description'], api_key)
            print("Customer Journey Analysis Result:")
            print(json.dumps(result, indent=2))
            
        elif test_case['type'] == 'workflow_orchestration':
            result = simulate_workflow_orchestration(test_case['description'], api_key)
            print("Workflow Orchestration Result:")
            print(json.dumps(result, indent=2))
            
        elif test_case['type'] == 'business_intelligence':
            result = simulate_business_intelligence_report(test_case['description'], api_key)
            print("Business Intelligence Report Result:")
            print(json.dumps(result, indent=2))
        
        print()

if __name__ == "__main__":
    main() 