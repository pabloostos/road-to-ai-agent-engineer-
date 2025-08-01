#!/usr/bin/env python3
"""
Exercise 3: Advanced Function Patterns

Implement advanced function calling patterns with multiple functions,
complex schemas, and function chaining capabilities.
"""

import json
from jsonschema import validate, ValidationError
from typing import Dict, Any, List, Optional

def define_advanced_schemas():
    """Define advanced function schemas for complex scenarios."""
    schemas = {
        "search_products": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Search query for products"
                },
                "category": {
                    "type": "string",
                    "enum": ["electronics", "clothing", "books", "home", "sports"],
                    "description": "Product category to search in"
                },
                "price_range": {
                    "type": "object",
                    "properties": {
                        "min": {"type": "number", "minimum": 0},
                        "max": {"type": "number", "minimum": 0}
                    },
                    "required": ["min", "max"]
                },
                "sort_by": {
                    "type": "string",
                    "enum": ["price", "rating", "name", "date"],
                    "default": "rating"
                }
            },
            "required": ["query"]
        },
        
        "add_to_cart": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "pattern": "^PROD-[0-9]{6}$"
                },
                "quantity": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100
                },
                "options": {
                    "type": "object",
                    "properties": {
                        "size": {"type": "string"},
                        "color": {"type": "string"},
                        "warranty": {"type": "boolean"}
                    }
                }
            },
            "required": ["product_id", "quantity"]
        },
        
        "calculate_shipping": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_id": {"type": "string"},
                            "quantity": {"type": "integer"},
                            "weight": {"type": "number"}
                        },
                        "required": ["product_id", "quantity"]
                    }
                },
                "destination": {
                    "type": "object",
                    "properties": {
                        "country": {"type": "string"},
                        "postal_code": {"type": "string"},
                        "city": {"type": "string"}
                    },
                    "required": ["country", "city"]
                },
                "shipping_method": {
                    "type": "string",
                    "enum": ["standard", "express", "overnight"]
                }
            },
            "required": ["items", "destination"]
        },
        
        "process_payment": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "minimum": 0.01
                },
                "currency": {
                    "type": "string",
                    "enum": ["USD", "EUR", "GBP", "JPY"],
                    "default": "USD"
                },
                "payment_method": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["credit_card", "paypal", "apple_pay"]
                        },
                        "card_number": {"type": "string"},
                        "expiry": {"type": "string"},
                        "cvv": {"type": "string"}
                    },
                    "required": ["type"]
                },
                "billing_address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                        "country": {"type": "string"},
                        "postal_code": {"type": "string"}
                    },
                    "required": ["street", "city", "country"]
                }
            },
            "required": ["amount", "payment_method"]
        }
    }
    return schemas

def validate_function_call(params: Dict[str, Any], schema: Dict[str, Any]) -> tuple[bool, str]:
    """Validate function parameters against schema."""
    try:
        validate(instance=params, schema=schema)
        return True, "Parameters are valid"
    except ValidationError as e:
        return False, f"Validation error: {e.message}"

def simulate_search_products(params: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate product search function."""
    query = params.get("query", "")
    category = params.get("category", "all")
    price_range = params.get("price_range", {})
    sort_by = params.get("sort_by", "rating")
    
    # Simulate search results
    results = [
        {
            "product_id": "PROD-123456",
            "name": f"Sample {query} Product",
            "price": 29.99,
            "rating": 4.5,
            "category": category
        },
        {
            "product_id": "PROD-789012",
            "name": f"Premium {query} Item",
            "price": 59.99,
            "rating": 4.8,
            "category": category
        }
    ]
    
    return {
        "function": "search_products",
        "results": results,
        "total_count": len(results),
        "query": query,
        "filters_applied": {
            "category": category,
            "price_range": price_range,
            "sort_by": sort_by
        }
    }

def simulate_add_to_cart(params: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate add to cart function."""
    product_id = params.get("product_id")
    quantity = params.get("quantity", 1)
    options = params.get("options", {})
    
    return {
        "function": "add_to_cart",
        "success": True,
        "cart_item": {
            "product_id": product_id,
            "quantity": quantity,
            "options": options,
            "added_at": "2024-01-15T10:30:00Z"
        },
        "cart_total": quantity * 29.99  # Simulated price
    }

def simulate_calculate_shipping(params: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate shipping calculation function."""
    items = params.get("items", [])
    destination = params.get("destination", {})
    shipping_method = params.get("shipping_method", "standard")
    
    # Calculate shipping based on method
    base_cost = 5.99
    if shipping_method == "express":
        base_cost = 12.99
    elif shipping_method == "overnight":
        base_cost = 24.99
    
    return {
        "function": "calculate_shipping",
        "shipping_cost": base_cost,
        "estimated_days": {
            "standard": 5,
            "express": 2,
            "overnight": 1
        }[shipping_method],
        "destination": destination,
        "method": shipping_method
    }

def simulate_process_payment(params: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate payment processing function."""
    amount = params.get("amount", 0)
    currency = params.get("currency", "USD")
    payment_method = params.get("payment_method", {})
    
    return {
        "function": "process_payment",
        "success": True,
        "transaction_id": "TXN-123456789",
        "amount": amount,
        "currency": currency,
        "payment_method": payment_method.get("type"),
        "processed_at": "2024-01-15T10:30:00Z"
    }

def execute_function(function_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a function based on its name."""
    function_map = {
        "search_products": simulate_search_products,
        "add_to_cart": simulate_add_to_cart,
        "calculate_shipping": simulate_calculate_shipping,
        "process_payment": simulate_process_payment
    }
    
    if function_name in function_map:
        return function_map[function_name](params)
    else:
        return {"error": f"Unknown function: {function_name}"}

def simulate_advanced_function_call(user_input: str) -> Optional[Dict[str, Any]]:
    """Simulate advanced function calling based on user input."""
    input_lower = user_input.lower()
    
    if "search" in input_lower and "product" in input_lower:
        if "electronics" in input_lower:
            return {
                "name": "search_products",
                "arguments": {
                    "query": "laptop",
                    "category": "electronics",
                    "price_range": {"min": 0, "max": 1000},
                    "sort_by": "price"
                }
            }
        elif "clothing" in input_lower:
            return {
                "name": "search_products",
                "arguments": {
                    "query": "shirt",
                    "category": "clothing",
                    "sort_by": "rating"
                }
            }
        else:
            return {
                "name": "search_products",
                "arguments": {
                    "query": "product",
                    "sort_by": "rating"
                }
            }
    
    elif "add" in input_lower and "cart" in input_lower:
        return {
            "name": "add_to_cart",
            "arguments": {
                "product_id": "PROD-123456",
                "quantity": 2,
                "options": {
                    "size": "M",
                    "color": "blue"
                }
            }
        }
    
    elif "shipping" in input_lower or "delivery" in input_lower:
        return {
            "name": "calculate_shipping",
            "arguments": {
                "items": [
                    {"product_id": "PROD-123456", "quantity": 1}
                ],
                "destination": {
                    "country": "USA",
                    "city": "New York",
                    "postal_code": "10001"
                },
                "shipping_method": "express"
            }
        }
    
    elif "pay" in input_lower or "payment" in input_lower:
        return {
            "name": "process_payment",
            "arguments": {
                "amount": 99.99,
                "currency": "USD",
                "payment_method": {
                    "type": "credit_card",
                    "card_number": "****-****-****-1234"
                },
                "billing_address": {
                    "street": "123 Main St",
                    "city": "New York",
                    "country": "USA"
                }
            }
        }
    
    return None

def run_advanced_tests():
    """Run advanced function calling tests."""
    test_cases = [
        {
            "name": "Search Electronics Products",
            "input": "Search for electronics products under $1000",
            "expected_function": "search_products"
        },
        {
            "name": "Add Item to Cart",
            "input": "Add this product to my cart",
            "expected_function": "add_to_cart"
        },
        {
            "name": "Calculate Shipping",
            "input": "Calculate shipping cost for express delivery",
            "expected_function": "calculate_shipping"
        },
        {
            "name": "Process Payment",
            "input": "Process payment with credit card",
            "expected_function": "process_payment"
        }
    ]
    return test_cases

def main():
    """Main function for Exercise 3."""
    print("Exercise 3: Advanced Function Patterns")
    print("=" * 45)
    
    # Define schemas
    schemas = define_advanced_schemas()
    print("Available functions:")
    for function_name in schemas.keys():
        print(f"  - {function_name}")
    print()
    
    # Run test cases
    test_cases = run_advanced_tests()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print("-" * 40)
        print(f"Input: {test_case['input']}")
        
        # Simulate function call
        function_call = simulate_advanced_function_call(test_case['input'])
        
        if function_call:
            function_name = function_call['name']
            arguments = function_call['arguments']
            
            print(f"Function detected: {function_name}")
            print(f"Arguments: {json.dumps(arguments, indent=2)}")
            
            # Validate parameters
            if function_name in schemas:
                is_valid, message = validate_function_call(arguments, schemas[function_name])
                print(f"Validation: {message}")
                
                if is_valid:
                    # Execute function
                    result = execute_function(function_name, arguments)
                    print("Function result:")
                    print(json.dumps(result, indent=2))
                else:
                    print("Function execution skipped due to validation error")
            else:
                print(f"Unknown function: {function_name}")
        else:
            print("No function call detected")
        
        print()

if __name__ == "__main__":
    main() 