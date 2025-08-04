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
    prompt = """
You are a business analyst analyzing customer interactions across multiple departments.
Create a comprehensive customer journey analysis that integrates data from:
- Customer Support (tickets, sentiment)
- Sales (lead scoring, call summaries)
- Marketing (campaign responses)
- Operations (incident impact)

Return a JSON object with:
- "customer_id": unique identifier
- "journey_stage": "awareness", "consideration", "purchase", "retention", or "advocacy"
- "department_touchpoints": list of interactions by department
- "overall_sentiment": "positive", "negative", or "neutral"
- "risk_score": 0-100 (likelihood of churn)
- "opportunity_score": 0-100 (upsell potential)
- "recommended_actions": list of next steps by department
- "escalation_needed": true/false

Customer Data:
"""
    return prompt

def create_workflow_orchestrator_prompt():
    """Create a prompt for orchestrating multi-department workflows."""
    prompt = """
You are a workflow orchestrator managing business processes across departments.
Based on the input, determine the optimal workflow sequence and assign tasks to appropriate departments.

Consider:
- Process priority and urgency
- Department capabilities and availability
- SLA requirements
- Resource allocation
- Handoff points

Return a JSON object with:
- "workflow_id": unique identifier
- "priority": "low", "medium", "high", or "critical"
- "departments_involved": list of departments
- "task_sequence": ordered list of tasks
- "estimated_duration": total time estimate
- "dependencies": task dependencies
- "success_metrics": list of KPIs to track
- "escalation_triggers": conditions for escalation

Workflow Request:
"""
    return prompt

def create_business_intelligence_prompt():
    """Create a prompt for generating business intelligence reports."""
    prompt = """
You are a business intelligence analyst creating comprehensive reports.
Synthesize data from multiple departments to provide actionable insights.

Include:
- Key performance indicators
- Trend analysis
- Cross-department correlations
- Risk assessments
- Opportunity identification
- Strategic recommendations

Return a JSON object with:
- "report_period": time period covered
- "executive_summary": high-level insights
- "department_performance": performance by department
- "trends": identified trends
- "risks": potential risks
- "opportunities": growth opportunities
- "recommendations": strategic actions
- "next_period_focus": priority areas

Business Data:
"""
    return prompt

def simulate_customer_journey_analysis(customer_data: str) -> Dict[str, Any]:
    """Simulate customer journey analysis without API call."""
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

def simulate_workflow_orchestration(workflow_request: str) -> Dict[str, Any]:
    """Simulate workflow orchestration without API call."""
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

def simulate_business_intelligence_report(business_data: str) -> Dict[str, Any]:
    """Simulate business intelligence report without API call."""
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
            result = simulate_customer_journey_analysis(test_case['description'])
            print("Customer Journey Analysis Result:")
            print(json.dumps(result, indent=2))
            
        elif test_case['type'] == 'workflow_orchestration':
            result = simulate_workflow_orchestration(test_case['description'])
            print("Workflow Orchestration Result:")
            print(json.dumps(result, indent=2))
            
        elif test_case['type'] == 'business_intelligence':
            result = simulate_business_intelligence_report(test_case['description'])
            print("Business Intelligence Report Result:")
            print(json.dumps(result, indent=2))
        
        print()

if __name__ == "__main__":
    main() 