#!/usr/bin/env python3
"""
Exercise 1: Basic Function Calling

Create a simple function calling system that demonstrates JSON schema definition
and simulates function calls without using external APIs.
"""

import json
from jsonschema import validate, ValidationError

def define_weather_function_schema():
    """Define the weather function schema."""
    schema = {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The temperature unit to use"
            }
        },
        "required": ["location"]
    }
    return schema

def validate_parameters(params, schema):
    """Validate input parameters using JSON schema."""
    try:
        validate(instance=params, schema=schema)
        return True, "Parameters are valid"
    except ValidationError as e:
        return False, f"Validation error: {e.message}"

def simulate_weather_api_call(location, units="celsius"):
    """Simulate a weather API call."""
    weather_data = {
        "location": location,
        "temperature": 22 if units == "celsius" else 72,
        "condition": "sunny",
        "humidity": 65,
        "units": units
    }
    return weather_data

def simulate_function_call(user_input):
    """Simulate a function call based on user input."""
    # This simulates what an LLM would do when given a function schema
    if "madrid" in user_input.lower():
        return {
            "name": "get_weather",
            "arguments": {
                "location": "Madrid",
                "units": "celsius"
            }
        }
    elif "tokyo" in user_input.lower() and "fahrenheit" in user_input.lower():
        return {
            "name": "get_weather",
            "arguments": {
                "location": "Tokyo",
                "units": "fahrenheit"
            }
        }
    elif "new york" in user_input.lower():
        return {
            "name": "get_weather",
            "arguments": {
                "location": "New York"
            }
        }
    else:
        return None

def main():
    """Main function for Exercise 1."""
    print("Exercise 1: Basic Function Calling")
    print("=" * 40)
    
    # Define function schema
    schema = define_weather_function_schema()
    print("Function schema defined:")
    print(json.dumps(schema, indent=2))
    print()
    
    # Test cases
    test_cases = [
        "What's the weather like in Madrid?",
        "Get weather for Tokyo in fahrenheit",
        "Weather in New York"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case}")
        print("-" * 30)
        
        # Simulate function call
        function_call = simulate_function_call(test_case)
        
        if function_call:
            print(f"Function call detected: {function_call['name']}")
            print(f"Arguments: {json.dumps(function_call['arguments'], indent=2)}")
            
            # Validate parameters
            is_valid, message = validate_parameters(function_call['arguments'], schema)
            print(f"Validation: {message}")
            
            if is_valid:
                # Execute function
                weather_data = simulate_weather_api_call(
                    function_call['arguments']['location'],
                    function_call['arguments'].get('units', 'celsius')
                )
                print("Weather data:")
                print(json.dumps(weather_data, indent=2))
            else:
                print("Function execution skipped due to validation error")
        else:
            print("No function call detected")
        
        print()

if __name__ == "__main__":
    main() 