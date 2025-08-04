#!/usr/bin/env python3
"""
Exercise 3: HR & Operations

Implement business prompts for HR and operations including
resume screening, incident classification, and policy Q&A.
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

def call_openrouter_api(api_key: str, prompt: str, max_tokens: int = 400) -> str:
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

def create_resume_screening_prompt():
    """Create a prompt for resume screening."""
    prompt = """You are an AI recruiter analyzing resumes for job positions.

Evaluate the candidate's fit for the specified role and return a structured assessment.
Consider:
- Relevant experience and skills
- Education and certifications
- Cultural fit indicators
- Red flags or concerns
- Overall recommendation

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "is_qualified": true|false,
  "years_experience": number,
  "key_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "red_flags": ["flag1", "flag2"],
  "recommendation": "hire|consider|reject",
  "confidence": 0.0-1.0
}

Job Position:
Resume:
"""
    return prompt

def create_incident_classifier_prompt():
    """Create a prompt for classifying business incidents."""
    prompt = """You are an operations AI classifying business incidents.

Categorize the incident and assess its impact on business operations.
Consider:
- Incident type and severity
- Affected systems or processes
- Business impact level
- Required response time
- Escalation needs

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "incident_type": "technical|security|operational|customer|other",
  "severity": "low|medium|high|critical",
  "business_impact": "minimal|moderate|significant|severe",
  "affected_systems": ["system1", "system2"],
  "response_time": "immediate|within_1_hour|within_4_hours|next_business_day",
  "escalation_required": true|false,
  "estimated_resolution_time": "hours|days|weeks"
}

Incident Description:
"""
    return prompt

def create_policy_qa_prompt():
    """Create a prompt for policy Q&A."""
    prompt = """You are an HR assistant answering employee policy questions.

Provide accurate, helpful responses based on company policies.
Guidelines:
- Be clear and concise
- Reference specific policy sections when possible
- Provide actionable next steps
- Maintain confidentiality
- Escalate complex issues when needed

IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
{
  "answer": "clear response to the question",
  "policy_reference": "relevant policy section",
  "next_steps": ["step1", "step2"],
  "escalation_needed": true|false,
  "confidence": 0.0-1.0
}

Employee Question:
"""
    return prompt

def simulate_resume_screening(resume_text: str, job_position: str, api_key: str = None) -> Dict[str, Any]:
    """Screen resumes using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_resume_screening_prompt() + f"Job Position: {job_position}\nResume: {resume_text}"
        
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
                        "is_qualified": False,
                        "years_experience": 0,
                        "key_skills": ["API response parsing issue"],
                        "missing_skills": ["Unable to parse response"],
                        "red_flags": ["Response format issue"],
                        "recommendation": "reject",
                        "confidence": 0.5
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "is_qualified": False,
                    "years_experience": 0,
                    "key_skills": ["JSON parsing error"],
                    "missing_skills": ["Response format issue"],
                    "red_flags": ["Parsing error"],
                    "recommendation": "reject",
                    "confidence": 0.5
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    resume_lower = resume_text.lower()
    job_lower = job_position.lower()
    
    # Simple screening logic
    years_experience = 0
    key_skills = []
    missing_skills = []
    red_flags = []
    
    # Extract experience
    if "years" in resume_lower or "experience" in resume_lower:
        years_experience = 3  # Simulated
    
    # Check for relevant skills
    if "python" in resume_lower or "programming" in resume_lower:
        key_skills.append("Python")
    if "data" in resume_lower or "analytics" in resume_lower:
        key_skills.append("Data Analysis")
    if "management" in resume_lower or "lead" in resume_lower:
        key_skills.append("Leadership")
    
    # Check for red flags
    if "gap" in resume_lower or "unemployed" in resume_lower:
        red_flags.append("Employment gaps")
    if "short" in resume_lower and "tenure" in resume_lower:
        red_flags.append("Short job tenures")
    
    # Determine qualification
    is_qualified = len(key_skills) >= 2 and len(red_flags) < 2
    recommendation = "hire" if is_qualified and len(red_flags) == 0 else "consider" if is_qualified else "reject"
    
    return {
        "is_qualified": is_qualified,
        "years_experience": years_experience,
        "key_skills": key_skills,
        "missing_skills": ["Communication", "Teamwork"] if len(key_skills) < 3 else [],
        "red_flags": red_flags,
        "recommendation": recommendation,
        "confidence": 0.8
    }

def simulate_incident_classification(incident_description: str, api_key: str = None) -> Dict[str, Any]:
    """Classify incidents using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_incident_classifier_prompt() + incident_description
        
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
                        "incident_type": "other",
                        "severity": "medium",
                        "business_impact": "moderate",
                        "affected_systems": ["API response parsing issue"],
                        "response_time": "within_4_hours",
                        "escalation_required": False,
                        "estimated_resolution_time": "days"
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "incident_type": "other",
                    "severity": "medium",
                    "business_impact": "moderate",
                    "affected_systems": ["JSON parsing error"],
                    "response_time": "within_4_hours",
                    "escalation_required": False,
                    "estimated_resolution_time": "days"
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    description_lower = incident_description.lower()
    
    # Determine incident type
    if any(word in description_lower for word in ["server", "system", "technical", "bug"]):
        incident_type = "technical"
        severity = "medium"
    elif any(word in description_lower for word in ["security", "breach", "hack", "unauthorized"]):
        incident_type = "security"
        severity = "high"
    elif any(word in description_lower for word in ["customer", "complaint", "service"]):
        incident_type = "customer"
        severity = "medium"
    else:
        incident_type = "operational"
        severity = "low"
    
    # Determine business impact
    if severity == "high":
        business_impact = "significant"
        response_time = "immediate"
        escalation_required = True
    elif severity == "medium":
        business_impact = "moderate"
        response_time = "within_4_hours"
        escalation_required = False
    else:
        business_impact = "minimal"
        response_time = "next_business_day"
        escalation_required = False
    
    return {
        "incident_type": incident_type,
        "severity": severity,
        "business_impact": business_impact,
        "affected_systems": ["Main application", "Database"] if incident_type == "technical" else ["Customer portal"],
        "response_time": response_time,
        "escalation_required": escalation_required,
        "estimated_resolution_time": "days" if severity == "high" else "hours"
    }

def simulate_policy_qa(question: str, api_key: str = None) -> Dict[str, Any]:
    """Answer policy questions using OpenRouter API or simulation."""
    if api_key:
        # Use real OpenRouter API
        prompt = create_policy_qa_prompt() + question
        
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
                        "answer": "API response parsing issue. Please contact HR directly.",
                        "policy_reference": "Unable to parse response",
                        "next_steps": ["Contact HR department"],
                        "escalation_needed": True,
                        "confidence": 0.5
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "answer": "JSON parsing error. Please contact HR directly.",
                    "policy_reference": "Response format issue",
                    "next_steps": ["Contact HR department"],
                    "escalation_needed": True,
                    "confidence": 0.5
                }
        except Exception as e:
            print(f"API Error: {e}")
            # Fall back to simulation
            pass
    
    # Fallback to simulation if no API key or API fails
    question_lower = question.lower()
    
    if "vacation" in question_lower or "pto" in question_lower:
        answer = "Employees are entitled to 20 PTO days per year. Submit requests at least 2 weeks in advance."
        policy_reference = "Section 3.2 - Paid Time Off"
        next_steps = ["Submit PTO request through HR portal", "Get manager approval"]
    elif "remote" in question_lower or "work from home" in question_lower:
        answer = "Remote work is allowed up to 3 days per week with manager approval."
        policy_reference = "Section 2.1 - Remote Work Policy"
        next_steps = ["Discuss with your manager", "Submit remote work agreement"]
    elif "expense" in question_lower or "reimbursement" in question_lower:
        answer = "Submit expense reports within 30 days with receipts. Use the expense portal for submissions."
        policy_reference = "Section 4.3 - Expense Reimbursement"
        next_steps = ["Gather receipts", "Submit through expense portal"]
    else:
        answer = "Please contact HR directly for specific policy questions."
        policy_reference = "General HR Policy"
        next_steps = ["Contact HR department"]
    
    return {
        "answer": answer,
        "policy_reference": policy_reference,
        "next_steps": next_steps,
        "escalation_needed": False,
        "confidence": 0.9
    }

def run_hr_operations_tests():
    """Run HR and operations workflow tests."""
    test_cases = [
        {
            "name": "Data Analyst Resume",
            "resume": "Senior Data Analyst with 5 years experience in Python, SQL, and data visualization. Led team of 3 analysts.",
            "job_position": "Senior Data Analyst",
            "type": "resume_screening"
        },
        {
            "name": "Technical Incident",
            "description": "Server downtime affecting customer portal. Users unable to access services for 2 hours.",
            "type": "incident_classification"
        },
        {
            "name": "Security Incident",
            "description": "Suspicious login attempts detected from unknown IP addresses. Potential security breach.",
            "type": "incident_classification"
        },
        {
            "name": "Vacation Policy Question",
            "question": "How many vacation days do I get per year and how do I request time off?",
            "type": "policy_qa"
        }
    ]
    return test_cases

def main():
    """Main function for Exercise 3."""
    print("Exercise 3: HR & Operations")
    print("=" * 35)
    
    # Load API key
    api_key = load_api_key()
    
    # Define prompts
    resume_prompt = create_resume_screening_prompt()
    incident_prompt = create_incident_classifier_prompt()
    policy_prompt = create_policy_qa_prompt()
    
    print("Business Prompts Created:")
    print("1. Resume Screening System")
    print("2. Incident Classifier")
    print("3. Policy Q&A Assistant")
    print()
    
    # Run test cases
    test_cases = run_hr_operations_tests()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        if test_case['type'] == 'resume_screening':
            print(f"Job Position: {test_case['job_position']}")
            print(f"Resume: {test_case['resume']}")
            print()
            result = simulate_resume_screening(test_case['resume'], test_case['job_position'], api_key)
            print("Resume Screening Result:")
            print(json.dumps(result, indent=2))
            
        elif test_case['type'] == 'incident_classification':
            print(f"Incident: {test_case['description']}")
            print()
            result = simulate_incident_classification(test_case['description'], api_key)
            print("Incident Classification Result:")
            print(json.dumps(result, indent=2))
            
        elif test_case['type'] == 'policy_qa':
            print(f"Question: {test_case['question']}")
            print()
            result = simulate_policy_qa(test_case['question'], api_key)
            print("Policy Q&A Result:")
            print(json.dumps(result, indent=2))
        
        print()

if __name__ == "__main__":
    main() 