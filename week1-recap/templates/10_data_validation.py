# Data Validation Templates
# Week 1 - Road to AI Agent Engineer

import re
from typing import Dict, Any, List, Optional

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """Validate that all required fields are present."""
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    return True

def validate_data_types(data: Dict[str, Any], type_schema: Dict[str, type]) -> bool:
    """Validate data types against schema."""
    for field, expected_type in type_schema.items():
        if field in data and not isinstance(data[field], expected_type):
            return False
    return True

def validate_string_length(text: str, min_length: int = 0, max_length: int = None) -> bool:
    """Validate string length."""
    if len(text) < min_length:
        return False
    if max_length and len(text) > max_length:
        return False
    return True

def validate_numeric_range(value: float, min_value: float = None, max_value: float = None) -> bool:
    """Validate numeric value is within range."""
    if min_value is not None and value < min_value:
        return False
    if max_value is not None and value > max_value:
        return False
    return True

def create_validation_schema(fields: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Create a validation schema."""
    return {
        "type": "object",
        "properties": fields,
        "required": [field for field, config in fields.items() if config.get("required", False)]
    } 