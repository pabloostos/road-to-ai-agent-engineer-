# Testing Templates
# Week 1 - Road to AI Agent Engineer

import time
from typing import Dict, Any, Callable

def test_api_connection(api_func: Callable, *args, **kwargs):
    """Test API connection."""
    try:
        start_time = time.time()
        result = api_func(*args, **kwargs)
        response_time = time.time() - start_time
        
        return {
            "success": True,
            "response_time": response_time,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def test_json_parsing(json_string: str):
    """Test JSON parsing."""
    try:
        import json
        parsed = json.loads(json_string)
        return {
            "success": True,
            "parsed_data": parsed
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": str(e)
        }

def test_schema_validation(data: Dict[str, Any], schema: Dict[str, Any]):
    """Test schema validation."""
    try:
        from jsonschema import validate
        validate(instance=data, schema=schema)
        return {"success": True}
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def run_test_suite(tests: list):
    """Run a suite of tests."""
    results = []
    for test in tests:
        result = test()
        results.append(result)
    return results

def benchmark_function(func: Callable, iterations: int = 10):
    """Benchmark function performance."""
    times = []
    for _ in range(iterations):
        start = time.time()
        func()
        times.append(time.time() - start)
    
    return {
        "average_time": sum(times) / len(times),
        "min_time": min(times),
        "max_time": max(times)
    } 