# Prompt Engineering Templates
# Week 1 - Road to AI Agent Engineer

def create_json_prompt(fields: list, description: str = ""):
    """Create a prompt for JSON output."""
    field_list = ", ".join([f"'{field}'" for field in fields])
    
    prompt = f"""Return the result as a JSON object with the following fields: {field_list}."""
    
    if description:
        prompt += f" {description}"
    
    prompt += " Respond with only the JSON, no explanations."
    
    return prompt

def create_api_simulation_prompt(method: str, endpoint: str, data: str = ""):
    """Create a prompt for API simulation."""
    prompt = f"""Simulate a {method} request to {endpoint}."""
    
    if data:
        prompt += f" Include this data: {data}"
    
    prompt += " Return the full HTTP response with headers and JSON body."
    
    return prompt

def create_business_prompt(task: str, output_format: str = "json"):
    """Create a business workflow prompt."""
    prompt = f"""You are a business AI assistant. {task}"""
    
    if output_format == "json":
        prompt += " Return your response as valid JSON."
    elif output_format == "markdown":
        prompt += " Format your response in Markdown."
    
    return prompt

def create_structured_prompt(role: str, task: str, format: str = "json"):
    """Create a structured prompt with role and task."""
    prompt = f"""You are {role}. {task}"""
    
    if format == "json":
        prompt += " Respond with valid JSON only."
    elif format == "markdown":
        prompt += " Use Markdown formatting."
    
    return prompt 