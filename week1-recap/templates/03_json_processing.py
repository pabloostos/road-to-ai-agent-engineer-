# JSON Processing Templates
# Week 1 - Road to AI Agent Engineer

import json
import re
from typing import Dict, Any, Optional

def extract_json_from_response(response: str) -> str:
    """Extract JSON from LLM response."""
    # Look for JSON in backticks
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    # Look for JSON without backticks
    json_match = re.search(r'\{.*?\}', response, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    return response

def parse_json_safely(json_string: str) -> Dict[str, Any]:
    """Safely parse JSON string."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Validate data against JSON schema."""
    try:
        from jsonschema import validate
        validate(instance=data, schema=schema)
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False

def create_simple_schema(properties: Dict[str, str], required: list = None) -> Dict[str, Any]:
    """Create a simple JSON schema."""
    schema = {
        "type": "object",
        "properties": properties,
        "additionalProperties": False
    }
    
    if required:
        schema["required"] = required
    
    return schema 