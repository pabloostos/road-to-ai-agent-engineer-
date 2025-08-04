# Business Workflow Templates
# Week 1 - Road to AI Agent Engineer

from typing import Dict, Any, List

def create_support_ticket_classifier():
    """Create support ticket classification prompt."""
    return """You are a customer support AI. Classify the following ticket into categories: ["Billing", "Technical", "Account", "Other"] and assign severity (1-5). Return JSON."""

def create_lead_scorer():
    """Create lead scoring prompt."""
    return """You are a sales AI. Score this lead (0-100) and provide summary. Return JSON with score and summary."""

def create_resume_screener():
    """Create resume screening prompt."""
    return """You are an HR AI. Analyze this resume for the given position. Return JSON with qualification status and key skills."""

def create_incident_classifier():
    """Create incident classification prompt."""
    return """You are an operations AI. Classify this incident by type and priority. Return JSON."""

def create_customer_journey_analyzer():
    """Create customer journey analysis prompt."""
    return """You are a business analyst. Analyze this customer journey across departments. Return JSON with insights."""

def create_workflow_orchestrator():
    """Create workflow orchestration prompt."""
    return """You are a workflow coordinator. Design a workflow for this request. Return JSON with task sequence."""

def create_business_intelligence():
    """Create business intelligence prompt."""
    return """You are a BI analyst. Generate insights from this data. Return JSON with key metrics and recommendations."""

def create_policy_qa():
    """Create policy Q&A prompt."""
    return """You are an HR policy expert. Answer this policy question accurately. Return JSON with answer and references.""" 