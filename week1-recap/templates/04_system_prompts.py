# System Prompt Templates
# Week 1 - Road to AI Agent Engineer

def create_basic_system_prompt(role: str, behavior: str = "", format: str = ""):
    """Create a basic system prompt."""
    prompt = f"You are {role}."
    
    if behavior:
        prompt += f" {behavior}"
    
    if format:
        prompt += f" {format}"
    
    return prompt

def create_role_prompt(role: str, background: str, personality: str, expertise: str):
    """Create a detailed role prompt."""
    return f"""You are {role}.

BACKGROUND: {background}
PERSONALITY: {personality}
EXPERTISE: {expertise}

Always stay in character and respond accordingly."""

def create_format_prompt(format_type: str):
    """Create format-specific prompts."""
    formats = {
        "json": "Always respond with valid JSON only. No explanations.",
        "markdown": "Format your response in Markdown.",
        "bullet": "Use bullet points for your response.",
        "numbered": "Use numbered lists for your response."
    }
    return formats.get(format_type, "")

def create_behavior_prompt(behavior_type: str):
    """Create behavior-specific prompts."""
    behaviors = {
        "friendly": "Be warm, supportive, and encouraging.",
        "professional": "Be formal, precise, and business-like.",
        "educational": "Explain concepts step-by-step with examples.",
        "concise": "Be brief and to the point."
    }
    return behaviors.get(behavior_type, "") 