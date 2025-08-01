#!/usr/bin/env python3
"""
Exercise 2: JSON Schema Validation

Implement comprehensive JSON schema validation for different data types
and complex validation scenarios.
"""

import json
from jsonschema import validate, ValidationError
from typing import Dict, Any, Tuple

def define_complex_schemas():
    """Define multiple complex JSON schemas for validation."""
    schemas = {
        "user_registration": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 20,
                    "pattern": "^[a-zA-Z0-9_]+$"
                },
                "email": {
                    "type": "string",
                    "format": "email"
                },
                "age": {
                    "type": "integer",
                    "minimum": 13,
                    "maximum": 120
                },
                "preferences": {
                    "type": "object",
                    "properties": {
                        "theme": {
                            "type": "string",
                            "enum": ["light", "dark", "auto"]
                        },
                        "notifications": {
                            "type": "boolean"
                        }
                    },
                    "required": ["theme"]
                }
            },
            "required": ["username", "email", "age"]
        },
        
        "product_order": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "pattern": "^ORD-[0-9]{6}$"
                },
                "items": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_id": {"type": "string"},
                            "quantity": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 100
                            },
                            "price": {
                                "type": "number",
                                "minimum": 0.01
                            }
                        },
                        "required": ["product_id", "quantity", "price"]
                    }
                },
                "shipping_address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                        "postal_code": {"type": "string"},
                        "country": {"type": "string"}
                    },
                    "required": ["street", "city", "country"]
                }
            },
            "required": ["order_id", "items", "shipping_address"]
        },
        
        "api_response": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["success", "error", "pending"]
                },
                "data": {
                    "type": "object",
                    "additionalProperties": True
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "metadata": {
                    "type": "object",
                    "properties": {
                        "version": {"type": "string"},
                        "request_id": {"type": "string"}
                    }
                }
            },
            "required": ["status", "timestamp"]
        }
    }
    return schemas

def validate_with_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate data against a JSON schema."""
    try:
        validate(instance=data, schema=schema)
        return True, "Data is valid"
    except ValidationError as e:
        return False, f"Validation error: {e.message} at path: {' -> '.join(str(p) for p in e.path)}"

def run_validation_tests():
    """Run various validation test cases."""
    test_cases = [
        {
            "name": "Valid User Registration",
            "data": {
                "username": "john_doe",
                "email": "john@example.com",
                "age": 25,
                "preferences": {
                    "theme": "dark",
                    "notifications": True
                }
            },
            "schema": "user_registration"
        },
        {
            "name": "Invalid User Registration - Bad Email",
            "data": {
                "username": "jane",
                "email": "invalid-email",
                "age": 30
            },
            "schema": "user_registration"
        },
        {
            "name": "Valid Product Order",
            "data": {
                "order_id": "ORD-123456",
                "items": [
                    {
                        "product_id": "PROD-001",
                        "quantity": 2,
                        "price": 29.99
                    }
                ],
                "shipping_address": {
                    "street": "123 Main St",
                    "city": "New York",
                    "country": "USA"
                }
            },
            "schema": "product_order"
        },
        {
            "name": "Invalid Product Order - Bad Order ID",
            "data": {
                "order_id": "INVALID-ID",
                "items": [
                    {
                        "product_id": "PROD-001",
                        "quantity": 2,
                        "price": 29.99
                    }
                ],
                "shipping_address": {
                    "street": "123 Main St",
                    "city": "New York",
                    "country": "USA"
                }
            },
            "schema": "product_order"
        },
        {
            "name": "Valid API Response",
            "data": {
                "status": "success",
                "data": {"user_id": 123},
                "timestamp": "2024-01-15T10:30:00Z",
                "metadata": {
                    "version": "1.0",
                    "request_id": "req-123"
                }
            },
            "schema": "api_response"
        }
    ]
    return test_cases

def main():
    """Main function for Exercise 2."""
    print("Exercise 2: JSON Schema Validation")
    print("=" * 45)
    
    # Define schemas
    schemas = define_complex_schemas()
    print("Available schemas:")
    for schema_name in schemas.keys():
        print(f"  - {schema_name}")
    print()
    
    # Run test cases
    test_cases = run_validation_tests()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        data = test_case['data']
        schema_name = test_case['schema']
        schema = schemas[schema_name]
        
        print(f"Data: {json.dumps(data, indent=2)}")
        print(f"Schema: {schema_name}")
        
        # Execute validation
        is_valid, message = validate_with_schema(data, schema)
        print(f"Validation result: {message}")
        
        print()

if __name__ == "__main__":
    main() 