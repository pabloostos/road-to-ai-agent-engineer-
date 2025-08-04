# Formatting Templates
# Week 1 - Road to AI Agent Engineer

from typing import Dict, Any, List

def format_json_response(data: Dict[str, Any], indent: int = 2) -> str:
    """Format data as JSON response."""
    import json
    return json.dumps(data, indent=indent)

def format_markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    """Format data as Markdown table."""
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    
    for row in rows:
        table += "| " + " | ".join(str(cell) for cell in row) + " |\n"
    
    return table

def format_bullet_list(items: List[str]) -> str:
    """Format items as bullet list."""
    return "\n".join(f"- {item}" for item in items)

def format_numbered_list(items: List[str]) -> str:
    """Format items as numbered list."""
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))

def format_code_block(code: str, language: str = "") -> str:
    """Format code as code block."""
    return f"```{language}\n{code}\n```"

def format_http_response(status_code: int, headers: Dict[str, str], body: str) -> str:
    """Format HTTP response."""
    response = f"HTTP/1.1 {status_code}\n"
    
    for key, value in headers.items():
        response += f"{key}: {value}\n"
    
    response += f"\n{body}"
    return response

def format_api_response(success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
    """Format standardized API response."""
    response = {"success": success}
    
    if success and data:
        response["data"] = data
    elif not success and error:
        response["error"] = error
    
    return response 