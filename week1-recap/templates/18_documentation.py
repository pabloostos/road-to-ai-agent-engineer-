# Documentation Templates
# Week 1 - Road to AI Agent Engineer

from typing import Dict, Any, List

def create_function_docstring(func_name: str, params: List[str], returns: str, description: str) -> str:
    """Create a function docstring."""
    docstring = f'"""\n{description}\n\n'
    
    if params:
        docstring += "Args:\n"
        for param in params:
            docstring += f"    {param}\n"
    
    if returns:
        docstring += f"\nReturns:\n    {returns}\n"
    
    docstring += '"""'
    return docstring

def create_class_docstring(class_name: str, description: str, methods: List[str] = None) -> str:
    """Create a class docstring."""
    docstring = f'"""\n{description}\n\n'
    
    if methods:
        docstring += "Methods:\n"
        for method in methods:
            docstring += f"    {method}\n"
    
    docstring += '"""'
    return docstring

def create_api_documentation(api_name: str, endpoints: List[Dict[str, Any]]) -> str:
    """Create API documentation."""
    doc = f"# {api_name} API Documentation\n\n"
    
    for endpoint in endpoints:
        doc += f"## {endpoint['method']} {endpoint['path']}\n\n"
        doc += f"{endpoint['description']}\n\n"
        
        if 'parameters' in endpoint:
            doc += "### Parameters\n"
            for param in endpoint['parameters']:
                doc += f"- `{param['name']}`: {param['description']}\n"
            doc += "\n"
        
        if 'response' in endpoint:
            doc += "### Response\n"
            doc += f"```json\n{endpoint['response']}\n```\n\n"
    
    return doc

def create_usage_example(func_name: str, params: Dict[str, Any], example_output: str) -> str:
    """Create usage example."""
    example = f"# Usage Example for {func_name}\n\n"
    example += "```python\n"
    example += f"{func_name}("
    
    param_str = ", ".join([f"{k}={v}" for k, v in params.items()])
    example += param_str
    example += ")\n"
    example += "```\n\n"
    example += "Output:\n"
    example += f"```\n{example_output}\n```"
    
    return example

def create_config_documentation(config: Dict[str, Any]) -> str:
    """Create configuration documentation."""
    doc = "# Configuration Documentation\n\n"
    
    for section, settings in config.items():
        doc += f"## {section.title()}\n\n"
        
        if isinstance(settings, dict):
            for key, value in settings.items():
                doc += f"- `{key}`: {value}\n"
        else:
            doc += f"{settings}\n"
        
        doc += "\n"
    
    return doc 