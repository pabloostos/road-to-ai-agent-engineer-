# Function Calling Templates
# Week 1 - Road to AI Agent Engineer

from typing import Dict, Any, List

def create_function_schema(name: str, description: str, parameters: Dict[str, Any]):
    """Create a function schema for LLM function calling."""
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": parameters,
            "required": list(parameters.keys())
        }
    }

def simulate_function_call(user_input: str, available_functions: List[Dict[str, Any]]):
    """Simulate function calling based on user input."""
    # Simple simulation - in real use, LLM would choose function
    for func in available_functions:
        if func["name"].lower() in user_input.lower():
            return {
                "name": func["name"],
                "arguments": {"query": user_input}
            }
    return None

def create_weather_function():
    """Create a weather function schema."""
    return create_function_schema(
        name="get_weather",
        description="Get weather information for a location",
        parameters={
            "location": {"type": "string"},
            "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
        }
    )

def create_calendar_function():
    """Create a calendar function schema."""
    return create_function_schema(
        name="create_event",
        description="Create a calendar event",
        parameters={
            "title": {"type": "string"},
            "date": {"type": "string", "format": "date"},
            "time": {"type": "string"}
        }
    ) 