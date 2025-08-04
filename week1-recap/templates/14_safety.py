# Safety Templates
# Week 1 - Road to AI Agent Engineer

import re
from typing import Dict, Any, List

def filter_sensitive_content(text: str) -> str:
    """Filter out sensitive information."""
    # Remove email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    
    # Remove phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    
    # Remove credit card numbers
    text = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CARD]', text)
    
    return text

def validate_safe_content(text: str) -> bool:
    """Validate content is safe."""
    unsafe_patterns = [
        r'\b(hack|crack|exploit|vulnerability)\b',
        r'\b(password|secret|key)\b',
        r'\b(admin|root|sudo)\b'
    ]
    
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    
    return True

def add_safety_disclaimer(response: str, context: str = "") -> str:
    """Add safety disclaimers to responses."""
    disclaimers = {
        "medical": "\n\nNote: This is for informational purposes only. Please consult a healthcare professional for medical advice.",
        "legal": "\n\nNote: This is not legal advice. Please consult a qualified attorney for legal matters.",
        "financial": "\n\nNote: This is not financial advice. Please consult a financial advisor for investment decisions."
    }
    
    if context in disclaimers:
        response += disclaimers[context]
    
    return response

def sanitize_input(user_input: str) -> str:
    """Sanitize user input."""
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        user_input = user_input.replace(char, '')
    
    # Limit length
    if len(user_input) > 1000:
        user_input = user_input[:1000]
    
    return user_input

def check_content_safety(content: str) -> Dict[str, Any]:
    """Check content for safety issues."""
    issues = []
    
    if not validate_safe_content(content):
        issues.append("Contains potentially unsafe content")
    
    if len(content) > 1000:
        issues.append("Content too long")
    
    return {
        "safe": len(issues) == 0,
        "issues": issues
    } 